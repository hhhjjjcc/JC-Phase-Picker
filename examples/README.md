# 示例数据

本目录包含用于测试和演示的示例数据。

## 目录结构

```
examples/
├── data/              # 示例波形数据
│   ├── event1/       # 事件1的数据
│   │   ├── station1.mseed
│   │   ├── station2.mseed
│   │   └── station3.mseed
│   └── event2/       # 事件2的数据
│       ├── station1.mseed
│       ├── station2.mseed
│       └── station3.mseed
├── picks/            # 示例拾取结果
│   ├── event1.csv
│   └── event2.csv
└── config/           # 示例配置文件
    ├── settings.json
    └── filters.json
```

## 数据说明

### 波形数据

- `event1/`: 包含事件1的三个台站记录
  - `station1.mseed`: 台站1的记录，信噪比高
  - `station2.mseed`: 台站2的记录，信噪比中等
  - `station3.mseed`: 台站3的记录，信噪比低

- `event2/`: 包含事件2的三个台站记录
  - `station1.mseed`: 台站1的记录，信噪比高
  - `station2.mseed`: 台站2的记录，信噪比中等
  - `station3.mseed`: 台站3的记录，信噪比低

### 拾取结果

- `event1.csv`: 事件1的拾取结果
  - 包含台站信息
  - 包含拾取时间
  - 包含拾取质量

- `event2.csv`: 事件2的拾取结果
  - 包含台站信息
  - 包含拾取时间
  - 包含拾取质量

### 配置文件

- `settings.json`: 示例设置文件
  - 包含UI设置
  - 包含绘图设置
  - 包含处理设置

- `filters.json`: 示例滤波器设置
  - 包含带通滤波器设置
  - 包含高通滤波器设置
  - 包含低通滤波器设置

## 使用方法

1. 复制示例数据到工作目录：
   ```bash
   cp -r examples/data/* /path/to/your/data/
   ```

2. 加载示例设置：
   ```bash
   cp examples/config/settings.json ~/.p_wave_picker/
   ```

3. 运行程序并打开示例数据：
   ```bash
   p_wave_picker
   ```

## 注意事项

- 示例数据仅用于测试和演示
- 实际使用时请替换为真实数据
- 配置文件可以根据需要修改 