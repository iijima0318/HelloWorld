import subprocess
import os

def clone_repository(git_url, directory):
    try:
        # ディレクトリが存在しない場合は作成
        if not os.path.exists(directory):
            os.makedirs(directory)
        # カレントディレクトリを変更
        os.chdir(directory)
        # Gitクローンコマンドを実行
        subprocess.run(["git", "clone", git_url], check=True)
        print("リポジトリが正常にクローンされました。")
    except subprocess.CalledProcessError as e:
        print(f"エラーが発生しました: {e}")
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")

# スクリプトの使用例
if __name__ == "__main__":
    git_url = input("クローンするGitHubリポジトリのURLを入力してください: ")
    directory = input("リポジトリを保存するディレクトリを入力してください: ")
    clone_repository(git_url, directory)

