"""
Memory Management - 内存管理工具

Purpose:
- Prevent OOM errors during long simulations
- Use ring buffers for fixed-memory storage
- Aggregate statistics periodically
"""

from collections import deque
from typing import Dict, List, Any, Optional
import numpy as np


class RingBuffer:
    """
    环形缓冲区 - 固定内存存储
    
    使用 deque 实现，自动覆盖旧数据
    """
    
    def __init__(self, max_size: int = 1000):
        """
        Args:
            max_size: 最大存储容量
        """
        self.max_size = max_size
        self.buffer = deque(maxlen=max_size)
    
    def append(self, item: Any) -> None:
        """添加项目（超出容量时自动覆盖最旧的）"""
        self.buffer.append(item)
    
    def extend(self, items: List[Any]) -> None:
        """批量添加项目"""
        self.buffer.extend(items)
    
    def get_all(self) -> List[Any]:
        """获取所有项目"""
        return list(self.buffer)
    
    def get_recent(self, n: int) -> List[Any]:
        """获取最近 n 个项目"""
        return list(self.buffer)[-n:]
    
    def __len__(self) -> int:
        return len(self.buffer)
    
    def clear(self) -> None:
        """清空缓冲区"""
        self.buffer.clear()


class StatisticsAggregator:
    """
    统计聚合器 - 定期聚合统计数据
    
    功能：
    - 累积原始数据
    - 定期聚合（每 N 步）
    - 只保存聚合结果，节省内存
    """
    
    def __init__(self, aggregation_interval: int = 50):
        """
        Args:
            aggregation_interval: 聚合间隔（步数）
        """
        self.aggregation_interval = aggregation_interval
        self.current_step = 0
        
        # 当前窗口的原始数据
        self.current_window = []
        
        # 聚合结果（只保存这些）
        self.aggregated_stats = []
        
        # 累计统计
        self.cumulative_stats = {
            'count': 0,
            'sum': 0.0,
            'sum_sq': 0.0,
            'min': float('inf'),
            'max': float('-inf')
        }
    
    def add(self, value: Any, step: Optional[int] = None) -> None:
        """
        添加数据点
        
        Args:
            value: 数据值
            step: 当前步数（可选，自动递增如果不提供）
        """
        if step is None:
            step = self.current_step
        
        self.current_step = step
        self.current_window.append(value)
        
        # 更新累计统计
        if isinstance(value, (int, float)):
            self.cumulative_stats['count'] += 1
            self.cumulative_stats['sum'] += value
            self.cumulative_stats['sum_sq'] += value ** 2
            self.cumulative_stats['min'] = min(self.cumulative_stats['min'], value)
            self.cumulative_stats['max'] = max(self.cumulative_stats['max'], value)
        
        # 检查是否需要聚合
        if len(self.current_window) >= self.aggregation_interval:
            self._aggregate()
    
    def _aggregate(self) -> None:
        """执行聚合"""
        if not self.current_window:
            return
        
        # 计算聚合统计
        values = np.array(self.current_window)
        
        agg = {
            'step_start': self.current_step - len(self.current_window),
            'step_end': self.current_step,
            'mean': float(np.mean(values)),
            'std': float(np.std(values)),
            'min': float(np.min(values)),
            'max': float(np.max(values)),
            'count': len(self.current_window)
        }
        
        # 添加高阶统计（如果可能）
        if len(values) > 2:
            try:
                agg['skewness'] = float(self._skewness(values))
                agg['kurtosis'] = float(self._kurtosis(values))
            except:
                agg['skewness'] = None
                agg['kurtosis'] = None
        
        self.aggregated_stats.append(agg)
        self.current_window = []
    
    @staticmethod
    def _skewness(x: np.ndarray) -> float:
        """计算偏度"""
        n = len(x)
        if n < 3:
            return 0.0
        mean = np.mean(x)
        std = np.std(x, ddof=1)
        if std == 0:
            return 0.0
        return (np.sum((x - mean) ** 3) / n) / (std ** 3)
    
    @staticmethod
    def _kurtosis(x: np.ndarray) -> float:
        """计算峰度"""
        n = len(x)
        if n < 4:
            return 3.0
        mean = np.mean(x)
        std = np.std(x, ddof=1)
        if std == 0:
            return 3.0
        return (np.sum((x - mean) ** 4) / n) / (std ** 4)
    
    def finalize(self) -> None:
        """ finalize: 聚合剩余数据"""
        if self.current_window:
            self._aggregate()
    
    def get_aggregated(self) -> List[Dict]:
        """获取所有聚合结果"""
        return self.aggregated_stats
    
    def get_cumulative_stats(self) -> Dict:
        """获取累计统计"""
        stats = self.cumulative_stats.copy()
        if stats['count'] > 0:
            stats['mean'] = stats['sum'] / stats['count']
            stats['variance'] = (stats['sum_sq'] / stats['count']) - (stats['mean'] ** 2)
            stats['std'] = np.sqrt(max(0, stats['variance']))
        return stats
    
    def clear(self) -> None:
        """清空所有数据"""
        self.current_step = 0
        self.current_window = []
        self.aggregated_stats = []
        self.cumulative_stats = {
            'count': 0,
            'sum': 0.0,
            'sum_sq': 0.0,
            'min': float('inf'),
            'max': float('-inf')
        }


class SimulationStateManager:
    """
    模拟状态管理器 - 统一管理模拟状态存储
    
    功能：
    - 管理多个 RingBuffer 和 StatisticsAggregator
    - 定期保存检查点
    - 内存使用监控
    """
    
    def __init__(
        self,
        buffer_size: int = 1000,
        aggregation_interval: int = 50,
        checkpoint_interval: int = 1000
    ):
        """
        Args:
            buffer_size: 环形缓冲区大小
            aggregation_interval: 统计聚合间隔
            checkpoint_interval: 检查点保存间隔
        """
        self.buffer_size = buffer_size
        self.aggregation_interval = aggregation_interval
        self.checkpoint_interval = checkpoint_interval
        
        # 状态存储
        self.buffers: Dict[str, RingBuffer] = {}
        self.aggregators: Dict[str, StatisticsAggregator] = {}
        
        # 检查点
        self.checkpoints = []
        self.current_step = 0
    
    def create_buffer(self, name: str, max_size: Optional[int] = None) -> RingBuffer:
        """创建新的环形缓冲区"""
        size = max_size if max_size is not None else self.buffer_size
        self.buffers[name] = RingBuffer(size)
        return self.buffers[name]
    
    def create_aggregator(self, name: str, interval: Optional[int] = None) -> StatisticsAggregator:
        """创建新的统计聚合器"""
        intv = interval if interval is not None else self.aggregation_interval
        self.aggregators[name] = StatisticsAggregator(intv)
        return self.aggregators[name]
    
    def record(self, name: str, value: Any, step: Optional[int] = None) -> None:
        """记录数据点"""
        if step is None:
            step = self.current_step
        
        # 记录到缓冲区
        if name in self.buffers:
            self.buffers[name].append(value)
        
        # 记录到聚合器
        if name in self.aggregators:
            self.aggregators[name].add(value, step)
    
    def step(self, step: Optional[int] = None) -> None:
        """前进一步"""
        if step is None:
            self.current_step += 1
        else:
            self.current_step = step
        
        # 检查是否需要保存检查点
        if self.current_step % self.checkpoint_interval == 0:
            self._save_checkpoint()
    
    def _save_checkpoint(self) -> None:
        """保存检查点（简化版本，只保存统计）"""
        checkpoint = {
            'step': self.current_step,
            'aggregated_stats': {
                name: agg.get_aggregated()
                for name, agg in self.aggregators.items()
            },
            'cumulative_stats': {
                name: agg.get_cumulative_stats()
                for name, agg in self.aggregators.items()
            }
        }
        self.checkpoints.append(checkpoint)
    
    def finalize(self) -> None:
        """ finalize: 聚合所有剩余数据，保存最终检查点"""
        for agg in self.aggregators.values():
            agg.finalize()
        
        self._save_checkpoint()
    
    def get_results(self) -> Dict:
        """获取所有结果"""
        return {
            'buffers': {name: buf.get_all() for name, buf in self.buffers.items()},
            'aggregated_stats': {name: agg.get_aggregated() for name, agg in self.aggregators.items()},
            'cumulative_stats': {name: agg.get_cumulative_stats() for name, agg in self.aggregators.items()},
            'checkpoints': self.checkpoints,
            'final_step': self.current_step
        }
    
    def clear(self) -> None:
        """清空所有状态"""
        for buf in self.buffers.values():
            buf.clear()
        for agg in self.aggregators.values():
            agg.clear()
        self.checkpoints = []
        self.current_step = 0
