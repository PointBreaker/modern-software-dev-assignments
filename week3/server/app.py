from mcp.server.fastmcp import FastMCP
import art

# 1. 创建一个 MCP 服务器实例
mcp = FastMCP("AsciiArtService")

# 2. 定义一个工具 (Tool)
# 装饰器会自动把函数注册为 MCP Tool
# 函数的 docstring 会自动变成 Tool 的描述给 AI 看
@mcp.tool()
def generate_ascii(text: str, font: str = "standard") -> str:
    """
    将文本转换为 ASCII 艺术字符画。
    Args:
        text: 要转换的文本内容
        font: 字体风格 (例如: "block", "lean", "standard")
    """
    try:
        # 调用 art 库生成字符画
        result = art.text2art(text, font=font)
        return result
    except Exception as e:
        return f"Error generating art: {str(e)}"

# 3. 运行服务器
if __name__ == "__main__":
    mcp.run(transport="stdio")
    