# DiscordBot_Notifier_VIX
for AWS Lambda

## AWS Lambdaにデプロイするための手順

1. Lamdba関数の作成

2. deploy用のディレクトリを作成する
```bash
mkdir deploy
```

3. srcコードをコピーする
```bash
Copy-Item .\src\lambda_function.py .\deploy\
```

4. 外部依存モジュールをインストールする
```bash
pip install -r requirements.txt --target ./deploy --no-user
```

5. zipファイルを作成する
```bash
Compress-Archive -Path .\deploy\* -DestinationPath lambda_deployment.zip -Force
```

6. AWS Lambdaにzipをアップロードする

7. トリガーの設定
   - イベントブリッジを追加
   - 月曜から金曜日の朝九時に実行されるようにcron式を設定
   - スケジュール式: `cron(0 0 ? * MON-FRI *)`