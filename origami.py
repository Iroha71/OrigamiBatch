from PIL import Image
import PySimpleGUI as sg
from typing import Any, Final, List
import glob
import os

ON_RESIZE: Final[str] = 'on_resize'

def get_target_imgs(img_dir: str, img_exr: str) -> List[str]:
  """指定のフォルダ内の画像リストを取得

  Args:
      img_dir (str): 対象のフォルダ
      img_exr (str): 取得する対象の画像拡張子

  Returns:
      List[str]: img_dir内の画像パスリスト
  """
  filter = f"*.{img_exr}"
  path = os.path.join(img_dir, filter)
  return glob.glob(path)
  
def resize_img(img: str, virtical: int, width: int):
  """画像をリサイズする

  Args:
      img (str): リサイズする画像のパス
      virtical (int): リサイズ高さ
      width (int): リサイズ幅
  """
  _img = Image.open(img)
  _img = _img.resize((int(virtical), int(width)))
  _img.save(img)

def receive_event(window: 'sg.Window'):
  """GUIイベントを受け付ける

  Args:
      window (sg.Window): GUIコンポーネント
  """
  while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
      break
    if event == ON_RESIZE:
      imgs: List[str] = get_target_imgs(values['inputFilePath'], 'tga')
      for img in imgs:
        resize_img(img, values['virtical'], values['width'])



def make_window():
  sg.theme('DarkAmber')
  layout = [
    [sg.Text('ファイル', size=(9, 1)), sg.Input(), sg.FolderBrowse('ファイルを選択', key='inputFilePath')],
    [sg.Text('画像サイズ')],
    [sg.Text('縦'), sg.InputText('', size=(5, 1), key='virtical'), sg.Text('横'), sg.InputText('', size=(5, 1), key='width')],
    [sg.Button('画像サイズを変更', key=ON_RESIZE)]
  ]
  window = sg.Window('sampble', layout)

  receive_event(window)

  window.close()

if __name__ == '__main__':
  make_window()