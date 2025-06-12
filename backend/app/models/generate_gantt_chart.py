from io import BytesIO
from datetime import datetime, timedelta, time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as mpatches
from backend.app.models.aws import convert_gantt_to_webp, upload_to_s3
from backend.app.db.connect import get_connection_pool
from zoneinfo import ZoneInfo

def create_eq_gantt_chart(station_name, start_datetime_window, end_datetime_window, x_start_limit=None, x_end_limit=None):
    cnx = None  
    cursor = None
    try:
        cnx = get_connection_pool()
        cursor = cnx.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                ei.eqp_code,
                et.eqp_type,
                si.module_name,
                si.station_name,
                st.status_name,
                es.work_date,
                es.start_time,
                es.end_time,
                es.hours
            FROM eqp_status es
            JOIN eqp_info ei ON es.eqp_id = ei.id
            JOIN eqp_types et ON ei.eqp_type_id = et.id
            JOIN station_info si ON ei.station_id = si.id
            JOIN status_types st ON es.status_id = st.id
            WHERE si.station_name = %s AND es.start_time >= %s AND es.start_time < %s
            ORDER BY et.eqp_type DESC, ei.eqp_code DESC, es.start_time
        """, (station_name,
            start_datetime_window.strftime('%Y-%m-%d %H:%M:%S'),
            end_datetime_window.strftime('%Y-%m-%d %H:%M:%S')
        ))

        tasks = cursor.fetchall()
        if not tasks:
            return {"message": "今天沒有工單資料"}

        eqid_data = {}
        eqid_order = []
        y_pos_map = {}
        current_y_pos = 0

        for task in tasks:
            eq_id = task.get("eqp_code")
            if not eq_id or not all(task.get(k) for k in ("start_time", "end_time", "hours", "status_name")):
                continue

            if eq_id not in y_pos_map:
                y_pos_map[eq_id] = current_y_pos
                eqid_order.append(eq_id)
                eqid_data[eq_id] = []
                current_y_pos += 1

            start_dt, end_dt = task["start_time"], task["end_time"]
            for key in ["start_time", "end_time"]:
                if isinstance(task[key], str):
                    try:
                        task[key] = datetime.strptime(task[key], '%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        continue

            eqid_data[eq_id].append({
                "start_dt": start_dt,
                "end_dt": end_dt,
                "duration_hours": float(task["hours"]),
                "status": str(task["status_name"])
            })

        if not eqid_data:
            return {"message": "無有效資料"}

        # 用來畫圖的資料
        status_colors = {
            'run': 'green',
            'down': 'red',
            'idle': 'gold'
        }
        default_color = 'gray'
        min_bar_width = 0.01  # 最小寬度（天）

        fig, ax = plt.subplots(figsize=(15, max(4, len(eqid_order) * 0.6)))

        for eq_id in eqid_order:
            y_pos = y_pos_map[eq_id]
            for task in eqid_data[eq_id]:
                start_dt, end_dt = task["start_dt"], task["end_dt"]
                duration_hours = task["duration_hours"]
                status = task["status"]
                duration_days = max(duration_hours / 24.0, min_bar_width)
                color = status_colors.get(status.lower(), default_color)

                ax.barh(
                    y=y_pos,
                    width=duration_days,
                    left=mdates.date2num(start_dt),
                    height=0.6,
                    align="center",
                    color=color,
                )

        ax.set_yticks(list(y_pos_map.values()))
        ax.set_yticklabels(list(y_pos_map.keys()))
        ax.xaxis_date()
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=4))
        ax.xaxis.set_minor_locator(mdates.HourLocator(interval=1))
        ax.grid(axis='x', linestyle='--', alpha=0.6)

        # 設定 x 軸範圍
        all_starts = [task["start_dt"] for eq_tasks in eqid_data.values() for task in eq_tasks]
        all_ends = [task["end_dt"] for eq_tasks in eqid_data.values() for task in eq_tasks]

        if x_start_limit is None:
            x_start_limit = min(all_starts)
        if x_end_limit is None:
            x_end_limit = max(all_ends)

        ax.set_xlim([mdates.date2num(x_start_limit), mdates.date2num(x_end_limit)])

        ax.set_title(f"{station_name} STATION", fontsize=20, fontweight='bold',)
        work_date = start_datetime_window.strftime('%Y-%m-%d')
        ax.set_xlabel(f"Work Date: {work_date}", fontsize=12)
        ax.set_ylabel("EQID", fontsize=12)

        plt.tight_layout(rect=[0, 0, 0.85, 1])

        legend_handles = [
            mpatches.Patch(color=status_colors.get('run', default_color), label='Run'),
            mpatches.Patch(color=status_colors.get('down', default_color), label='Down'),
            mpatches.Patch(color=status_colors.get('idle', default_color), label='Idle'),
        ]
        ax.legend(handles=legend_handles, title="STATUS", loc='upper left', bbox_to_anchor=(1.05, 1))

        buf = BytesIO()
        plt.savefig(buf, format="png", bbox_inches='tight', dpi=150)
        buf.seek(0)
        plt.close(fig)

        return [buf, station_name, work_date]

    except Exception as e:
        print(f"[ERROR] 生成圖表時發生錯誤: {e}")
        return {"message": f"生成圖表時發生錯誤: {e}"}
    
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()


def insert_gantt_chart_data(station_name: str, work_date: str, image_url: str):
    try:
        cnx = get_connection_pool()  
        cursor = cnx.cursor(dictionary=True)

        query_sql = """
            SELECT id, station_name FROM station_info
            WHERE station_name = %s
            """
        
        cursor.execute(query_sql, (station_name,))
        station_id = cursor.fetchone()
        print(station_id)
        
        insert_query = """
            INSERT INTO `gantt_charts`
            (
                `station_id`,
                `work_date`,
                `image_url`
                )
                VALUES (%s, %s, %s)
            """
        cursor.execute(insert_query, (station_id.get("id"), work_date, image_url))
        cnx.commit()

    except Exception as e:
        print(f"錯誤: {e}")
        return None
    
    finally:
        try:
            cursor.close()
            cnx.close()
        except:
            pass


def get_gantt_chart_data(station_name, work_date):
    try:
        cnx = get_connection_pool()  
        cursor = cnx.cursor(dictionary=True)  

        select_query = """
            SELECT gc.*, si.station_name FROM `gantt_charts` gc 
            LEFT JOIN `station_info` si
            ON gc.station_id = si.id
            WHERE si.station_name = %s
            AND gc.work_date = %s
            """
        cursor.execute(select_query, (station_name, work_date))
        gantt_chart_data = cursor.fetchone()

        return gantt_chart_data

    except Exception as e:
        print(f"錯誤: {e}")
        return None
    
    finally:
        try:
            cursor.close()
            cnx.close()
        except:
            pass


async def upload_gantt_to_s3(img_buf: list): 

    file_webp_io = convert_gantt_to_webp(img_buf[0])

    if file_webp_io:
        webp_filename = f"{img_buf[2]}-{img_buf[1]}-gantt-chart.webp"
        webp_content_type = "image/webp"

        img_url = await upload_to_s3(file_webp_io, webp_filename, webp_content_type)

        insert_gantt_chart_data(img_buf[1], img_buf[2], img_url)

        return {"text": webp_filename, "img_url": img_url}
    else:
        print("WebP 轉換失敗。")
        return {"text": "WebP 轉換失敗。", "img_url": None}
    
async def generate_gantt_chart():
    station_list = [
        "CPU",
        "RAM",
        "ROM",
        "GPU",
        "PSU",
        "CLS",
        "CWG",
        "CCA",
        "PKG",
    ]
    tz = ZoneInfo("Asia/Taipei")
    today = datetime.now(tz).date()
    insert_work_date = today - timedelta(days=1)

    for station in station_list:
        start_dt = datetime.combine(insert_work_date, time(7, 0)).replace(tzinfo=tz)
        
        end_dt = start_dt + timedelta(days=1)

        img_buf = create_eq_gantt_chart(station, start_dt, end_dt)

        try:
            await upload_gantt_to_s3(img_buf)
            print(f"{start_dt}-{station}-gantt-chart 成功上傳")
        except Exception as e:
            print(e)
            print("上傳失敗")
