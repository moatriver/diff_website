# 差分確認通知スクリプト

指定されたウェブサイトの差分を確認しSlackに通知するPythonスクリプトです。  
定期実行はOS依存です。Windowsでの動作は想定していません。

# おことわり

短期間に連続して使用する場合**DoS攻撃**にも転用できてしまうため、**使用には十分に注意してください。**  
このスクリプトファイルを使用して攻撃が行われた(または意図せず同等のことをしてしまった)場合、製作者は一切の責任を持ちません。

## フォルダ階層

┳diff_website.py : メインスクリプト  
┣sitedata.csv : 各サイトのフォルダ名とURLを保存するCSVファイル  
┗diff_data/ : 比較ファイルとログを保存するためのフォルダ  
&emsp;┗各サイト名のフォルダ  
&emsp;&emsp;┣new/ : サイトの最新ファイルを一時的に保存しておくフォルダ  
&emsp;&emsp;┗old/ : 直近の比較元ファイルと変更前のログを保存しておくフォルダ  

## CSV構造

- sitedata.csv
    - 1列目 フォルダ名
    - 2列目 URL
    - 3列目以降 diff実行結果のうち除外したい結果の指定 行数(a,d,cのどれか)行数 の形式

## JSON構造

XXXX-XXXX-XXX-XXXXをslackアプリのAPIキーに書き換え

```
{
    "slack_api" : "XXXX-XXXX-XXX-XXXX"
}
```