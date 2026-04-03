"""
Error Handling - 错误处理工具

Purpose:
- Standardize error handling across the codebase
- Provide meaningful error messages
- Enable graceful degradation
"""

from typing import Optional, Callable, Any
from contextlib import contextmanager
import logging
import time

# 配置日志
logger = logging.getLogger(__name__)


class SimulationError(Exception):
    """基础模拟错误"""
    pass


class ConfigurationError(SimulationError):
    """配置错误"""
    pass


class ConvergenceError(SimulationError):
    """收敛错误"""
    pass


class DataError(SimulationError):
    """数据错误"""
    pass


class ValidationError(SimulationError):
    """验证错误"""
    pass


def validate_config(config: dict, required_fields: list) -> None:
    """
    验证配置完整性
    
    Args:
        config: 配置字典
        required_fields: 必填字段列表
    
    Raises:
        ConfigurationError: 如果缺少必填字段
    """
    missing = [field for field in required_fields if field not in config]
    if missing:
        raise ConfigurationError(f"Missing required configuration fields: {missing}")


def validate_range(value: float, min_val: Optional[float], max_val: Optional[float], 
                   param_name: str) -> None:
    """
    验证参数范围
    
    Args:
        value: 参数值
        min_val: 最小值（None 表示无限制）
        max_val: 最大值（None 表示无限制）
        param_name: 参数名称
    
    Raises:
        ValidationError: 如果超出范围
    """
    if min_val is not None and value < min_val:
        raise ValidationError(f"{param_name} ({value}) is below minimum ({min_val})")
    
    if max_val is not None and value > max_val:
        raise ValidationError(f"{param_name} ({value}) is above maximum ({max_val})")


@contextmanager
def simulation_timeout(timeout_seconds: int, operation_name: str = "Simulation"):
    """
    超时控制上下文管理器
    
    Args:
        timeout_seconds: 超时时间（秒）
        operation_name: 操作名称
    
    Raises:
        TimeoutError: 如果超时
    
    Example:
        with simulation_timeout(300, "Calibration"):
            run_calibration()
    """
    import signal
    
    def handler(signum, frame):
        raise TimeoutError(f"{operation_name} exceeded {timeout_seconds}s timeout")
    
    # 设置信号处理器
    old_handler = signal.signal(signal.SIGALRM, handler)
    signal.alarm(timeout_seconds)
    
    try:
        yield
    finally:
        # 恢复原处理器
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old_handler)


@contextmanager
def error_handler(operation_name: str, on_error: Optional[Callable] = None,
                   retry_count: int = 0, default_return: Any = None):
    """
    错误处理上下文管理器
    
    Args:
        operation_name: 操作名称
        on_error: 错误回调函数
        retry_count: 重试次数
        default_return: 默认返回值（如果失败）
    
    Example:
        with error_handler("Calibration", retry_count=3):
            result = run_calibration()
    """
    attempt = 0
    
    while attempt <= retry_count:
        try:
            yield
            return
        except Exception as e:
            attempt += 1
            
            if attempt <= retry_count:
                logger.warning(f"{operation_name} failed (attempt {attempt}/{retry_count+1}): {e}")
                time.sleep(1)  # 等待 1 秒后重试
            else:
                logger.error(f"{operation_name} failed after {retry_count+1} attempts: {e}")
                
                if on_error:
                    on_error(e)
                
                if default_return is not None:
                    return default_return
                
                raise


def safe_execute(func: Callable, *args, default_return: Any = None, 
                 **kwargs) -> Any:
    """
    安全执行函数（捕获所有异常）
    
    Args:
        func: 要执行的函数
        *args: 位置参数
        default_return: 失败时的默认返回值
        **kwargs: 关键字参数
    
    Returns:
        函数返回值，或失败时的默认值
    
    Example:
        result = safe_execute(risky_function, arg1, default_return=None)
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(f"Error executing {func.__name__}: {e}")
        return default_return


class GracefulDegradation:
    """
    优雅降级管理器
    
    当某些功能失败时，提供降级方案
    """
    
    def __init__(self):
        self.fallbacks = {}
        self.failures = []
    
    def register_fallback(self, feature_name: str, fallback_func: Callable) -> None:
        """
        注册降级方案
        
        Args:
            feature_name: 功能名称
            fallback_func: 降级函数
        """
        self.fallbacks[feature_name] = fallback_func
    
    def execute(self, feature_name: str, primary_func: Callable, 
                *args, **kwargs) -> Any:
        """
        执行功能（失败时降级）
        
        Args:
            feature_name: 功能名称
            primary_func: 主要功能函数
            *args: 位置参数
            **kwargs: 关键字参数
        
        Returns:
            主要功能或降级功能的返回值
        """
        try:
            return primary_func(*args, **kwargs)
        except Exception as e:
            self.failures.append({
                'feature': feature_name,
                'error': str(e),
                'timestamp': time.time()
            })
            
            if feature_name in self.fallbacks:
                logger.warning(f"{feature_name} failed, using fallback: {e}")
                return self.fallbacks[feature_name](*args, **kwargs)
            else:
                logger.error(f"{feature_name} failed with no fallback: {e}")
                raise
    
    def get_failure_report(self) -> list:
        """获取失败报告"""
        return self.failures.copy()


# 使用示例
if __name__ == "__main__":
    # 配置验证示例
    config = {'n_agents': 100, 'n_days': 252}
    try:
        validate_config(config, ['n_agents', 'n_days', 'random_seed'])
    except ConfigurationError as e:
        print(f"配置错误：{e}")
    
    # 范围验证示例
    try:
        validate_range(0.5, 0, 1, 'herding_strength')
        print("参数验证通过")
    except ValidationError as e:
        print(f"验证错误：{e}")
    
    # 超时控制示例
    try:
        with simulation_timeout(5, "Test"):
            time.sleep(10)  # 这会超时
    except TimeoutError as e:
        print(f"超时：{e}")
    
    # 错误处理示例
    with error_handler("Test Operation", retry_count=2):
        raise ValueError("测试错误")
    
    # 优雅降级示例
    degradation = GracefulDegradation()
    degradation.register_fallback("complex_calc", lambda x: x * 2)
    
    result = degradation.execute("complex_calc", lambda x: 1/0, 5)
    print(f"降级结果：{result}")
