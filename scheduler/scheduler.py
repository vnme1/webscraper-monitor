"""
작업 스케줄러
"""
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from config import settings
from utils import setup_logger

logger = setup_logger(__name__)

class TaskScheduler:
    """작업 스케줄러 관리"""
    
    def __init__(self):
        self.scheduler = BlockingScheduler()
    
    def add_job(self, func, interval_minutes: int = None):
        """
        주기적 작업 추가
        
        Args:
            func: 실행할 함수
            interval_minutes: 실행 간격(분), None이면 설정값 사용
        """
        minutes = interval_minutes or settings.SCHEDULE_INTERVAL_MINUTES
        
        self.scheduler.add_job(
            func,
            trigger=IntervalTrigger(minutes=minutes),
            id=func.__name__,
            name=f"{func.__name__} (매 {minutes}분)",
            replace_existing=True
        )
        
        logger.info(f"작업 추가: {func.__name__} - 매 {minutes}분마다 실행")
    
    def start(self):
        """스케줄러 시작"""
        try:
            logger.info("스케줄러 시작")
            self.scheduler.start()
        except KeyboardInterrupt:
            logger.info("스케줄러 종료")
            self.scheduler.shutdown()
    
    def run_once(self, func):
        """즉시 한 번 실행"""
        logger.info(f"즉시 실행: {func.__name__}")
        func()