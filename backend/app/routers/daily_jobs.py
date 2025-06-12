from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from backend.app.models.daily_oee_moving import process_oee_data
from backend.app.models.generate_eqp_status import generate_eqp_status
from backend.app.models.generate_gantt_chart import generate_gantt_chart
from backend.app.models.generate_eqp_wip import generate_eqp_wip
from backend.app.models.updated_temp_oee import generate_temp_oee

scheduler = AsyncIOScheduler(timezone="Asia/Taipei")

def start_daily_jobs():

    scheduler.add_job(
        generate_eqp_status,
        CronTrigger(hour=6, minute=30),
        id="generate_eqp_status_job",
        replace_existing=True
    )

    scheduler.add_job(
        generate_gantt_chart,
        CronTrigger(hour=6, minute=36),
        id="generate_gantt_chart_job",
        replace_existing=True
    )

    scheduler.add_job(
        generate_eqp_wip,
        CronTrigger(hour=6, minute=39),
        id="generate_eqp_wip_job",
        replace_existing=True
    )

    scheduler.add_job(
        generate_temp_oee,
        CronTrigger(hour=23, minute=28),
        id="generate_temp_oee_job",
        replace_existing=True
    )

    scheduler.add_job(
        process_oee_data,
        CronTrigger(hour=6, minute=45),
        id="daily_oee_job",
        replace_existing=True
    )

    scheduler.start()
    print("所有 APScheduler 任務完成")
