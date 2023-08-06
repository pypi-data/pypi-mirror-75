# SYL_L_001_0排序_7堆排序

- 调整函数：adjustHeap(array, i, length)，对堆中第i个节点进行调整（给他找到它应该属于的位置）
- 排序函数sort(array)，对堆中每个非叶子🍃节点，都进行adjustHeap，则堆建立完成
- 排序过程：
```python
    for j in range(len(array) - 1, 0, -1):
        # 一开始最大元素是[0]，然后被换到最后一个
        # 从n-0，不断和[0]元素交换，重新堆排序（既把第2、3..n大的翻转到最上面）
        array[0], array[j] = array[j], array[0]
        adjustHeap(array, 0, j)
```

