# langchain-ai/langchain 2024-08-29

## 主要变更
* 更新了milvus.py文件。
* prompty工具的核心版本被提升。
* 发布了prompty的0.0.3版本。
* 在Azure AI搜索结果中添加了ID字段。
* 将ai21工具迁移到外部repo。
* ollama工具的核心版本被提升。
* 添加了max_iteration参数并处理解析错误。
* 更新了ChatAnthropic示例的文档，修正了语法错误。
* 发布了多个社区版本：0.2.14、0.2.13、0.2.15、0.1.6、0.1.23。
* 优化了xinference LLM的导入。
* 改进了`PineconeHybridSearchRetriever`的API文档。
* 修复了Amazon OpenSearch Serverless（AOSS）用于语义缓存存储的功能。
* 新增了约束COT评估器。
* 修复了一些文档中的小问题。
* 发现并修复了bug。
* 将databricks相关内容移到了合作伙伴repo。

## 处理的问题
* 解决了多个bug，包括文件中的语法错误。
* 修复了Azure AI搜索结果中缺失ID的问题。
* 处理了解析错误的情况。
* 优化了部分工具的导入和使用方式。

## 总结
在这段时间内，langchain项目实施了多项更新和优化，解决了一些遗留问题，提升了工具的稳定性和可用性。整体来说，项目动态活跃，开发者在不断改进功能和修复bug。