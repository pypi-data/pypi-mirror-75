# mpkg

一个简单的包管理器

mpkg 主要用于下载最新的软件，对安装软件的支持不佳，不支持卸载软件

暂不支持安装 wget, curl 等

## Demo

```bash
pip install mpkg
mpkg set sources --list
mpkg sync
mpkg list

pip install mpkg
mpkg config
```

## 使用说明

安装过程中出现 warning 仍认为安装成功

### mpkg config

加载非 json 源之前需要运行`mpkg set unsafe yes`，否则自动跳过。此外，json 源也未必安全，请留意下载时出现的 url。

注意：同类源的文件名（sources 源除外）不能相同。例如：`http://example1.com/e.json` 与 `https://example2.com/e.json` 会下载至相同文件夹，发生冲突。本地源直接读取文件，一般不会冲突（zip 解压时可能冲突）。

非本地源的文件名冲突可以通过特殊语法规避，例如：源 `http://[::1]:8081/intel.py->example.py` 代表将 `intel.py` 保存为 `example.py`

### 部分错误说明

#### warning: cannot find {pkg}

同步后的软件列表里找不到之前安装过的软件，常发生于软件源被修改后。可使用`mpkg remove {pkg}`解决

## 高级选项

### mpkg set

mpkg set --args soft "/S && D:\test.bat"

### 参数说明

#### {filepath}

引号与空格

### 文件说明

#### config.json

## 开发说明

### 软件源

支持以 .json, .py, .zip, .sources 结尾的四种源，除 .zip 外的文件均为文本，要求以 utf8 编码

#### json 源

json 地址若以 http 开头，则会同时请求 `文件名.ver` 文件（如：`https://example.com/example.json.ver`）。若不以 http 开头则识别为本地地址（建议使用绝对路径），不读取 .ver 文件，程序会直接从输入的地址导入信息。

.ver 文件使用 utf8 编码，内容为一个数字。若请求结果比之前大或请求失败，则会下载新的源文件。

json 格式如下，要求 id 唯一且不使用大小写区分 id

``` json
{"packages": [{"id": "NvidiaDriver.64bit",
               "ver": "451.48",
               "links": ["https://us.download.nvidia.com/Windows/451.48/451.48-notebook-win10-64bit-international-dch-whql.exe"],
               "date": "2020-06-24",
               "changelog": "https://us.download.nvidia.com/Windows/451.48/451.48-win10-win8-win7-release-notes.pdf", "name": "rtx"},
               {"id": "abc_v0.1",
                "ver": "test",
                "links": ["link1", "link2"]}]}
```

#### py 源

py 文件请求规则与 json 相同

编写代码时只能用 mpkg.utils.GetPage 获取页面。可以使用 lxml, BeautifulSoup 解析页面。

类名必须使用 Package，类必须有参数 id 且要求 id 唯一，文件名不能与其他 .py 文件相同，建议与 id 保持一致

必须定义 _prepare 函数并在其中生成 self.ver, self.links

#### zip 源

zip 文件请求规则与 json 相同

zip 文件中需要包含 packages 文件夹，packages 文件夹中只能包含 py 文件或 json 文件

程序支持加载从 github 下载的 master.zip，但必须通过 sources 源（无法获取 master.zip.ver）且以特殊语法加载此类源，否则会因文件名相同造成未知 bug

示例如下，在 master.zip 后加`->`与新的文件名

```json
{"http://[::1]:8081/master.zip->example.zip": 1}
```

#### sources 源

sources 源不请求 .ver 文件，每次同步时都会请求 sources 源，文件名可以相同

书写规则同 json，其中 key 代表 py, json 或 zip 源的地址，value 代表 ver，当 value 为 -1 时会请求 key 所对应的 .ver 文件

```json
{"D:\\Docs\\nv.py": -1,
 "http://[::1]:8081/intel.py": 1}
```

#### 总结

一般而言，
