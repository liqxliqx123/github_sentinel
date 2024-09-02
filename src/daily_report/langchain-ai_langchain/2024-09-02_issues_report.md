#  langchain-ai/langchain on 2024-09-02

## 主要变更
* 修复了 HuggingFace pipeline 模型属性相关的 bug。
* 更新了文档，修复了 Cassandra 的错误拼写以及一些未使用的导入语句。
* 改进了对 Serializable 字段的处理，使其能够处理无法转换为 bool 的字段。 

## 处理的问题
*  自查询检索器在使用 QdrantVectorStore 类型时不支持问题得到了关注。



## 总结
该项目最近进行了文档修复和功能优化，主要集中在 HuggingFace pipeline 和 Serializable 的改进。 也有一些 bug 被报告并关注，例如自查询检索器的类型限制问题。

