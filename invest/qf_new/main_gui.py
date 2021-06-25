# -*- coding: utf-8 -*-


import PySimpleGUI as sg

layout = []


def time_now():
    import time
    # 这个案例中有很多值得借鉴的东西
    # 比如
    '''
    sg.ChangeLookAndFeel('Black')
    sg.SetOptions(element_padding=(0, 0))
    sg.Button('Pause', key='button', button_color=('white', '#001480')
    window = sg.Window('Running Timer', layout, no_titlebar=True, auto_size_buttons=False, keep_on_top=True,
                       grab_anywhere=True)'''

    """
     计时器桌面小部件创建一个始终位于其他窗口顶部的浮动计时器可以通过抓住窗口上的任意位置来移动它，该示例很好地说明了如何使用SimpleGUI进行无阻塞的轮询程序，可在Pi上运行时用于轮询硬件
      当计时器刻度是由PySimpleGUI的“超时”机制生成时，实际值
       显示的计时器的一部分来自系统计时器time.time（）。 这保证了
       无论PySimpleGUI计时器刻度的准确性如何，都会显示准确的时间值。 如果
       如果不使用此设计，则显示的时间值将缓慢偏移时间
       它需要执行PySimpleGUI读取和更新调用（不好！）
      注意-使用退出按钮退出时，您会得到一条警告消息。
      它将类似于：无效的命令名称\“ 1616802625480StopMove \”
    """

    # ----------------  Create Form  ----------------
    sg.ChangeLookAndFeel('Black')
    sg.SetOptions(element_padding=(0, 0))

    layout = [[sg.Text('')],
              [sg.Text('', size=(8, 2), font=('Helvetica', 20), justification='center', key='text')],
              [sg.Button('Pause', key='button', button_color=('white', '#001480')),
               sg.Button('Reset', button_color=('white', '#007339'), key='Reset'),
               sg.Exit(button_color=('white', 'firebrick4'), key='Exit')]]

    window = sg.Window('Running Timer', layout, no_titlebar=True, auto_size_buttons=False, keep_on_top=True,
                       grab_anywhere=True)

    # ----------------  main loop  ----------------
    current_time = 0
    paused = False
    start_time = int(round(time.time() * 100))
    while True:
        # --------- Read and update window --------
        if not paused:
            event, values = window.read(timeout=10)
            current_time = int(round(time.time() * 100)) - start_time
        else:
            event, values = window.read()
        if event == 'button':
            event = window[event].GetText()
        # --------- Do Button Operations --------
        if event is None or event == 'Exit':  # ALWAYS give a way out of program
            break
        if event == 'Reset':
            start_time = int(round(time.time() * 100))
            current_time = 0
            paused_time = start_time
        elif event == 'Pause':
            paused = True
            paused_time = int(round(time.time() * 100))
            element = window['button']
            element.update(text='Run')
        elif event == 'Run':
            paused = False
            start_time = start_time + int(round(time.time() * 100)) - paused_time
            element = window['button']
            element.update(text='Pause')

        # --------- Display timer in window --------
        window['text'].update('{:02d}:{:02d}.{:02d}'.format((current_time // 100) // 60,
                                                            (current_time // 100) % 60, current_time % 100))


def the_gui():
    layout.append([sg.Text('  请在左侧操作  ', size=(25, 1), font=("Helvetica", 20))])

    layout.append([sg.B('Plot'), sg.Cancel(), sg.Button('Popup')])
    layout.append([sg.Image(key='-IMAGE-')])
    layout.append([sg.RButton('Create', size=(20, 2))])

    window = sg.Window('量化工具', finalize=True).Layout(layout)
    while True:
        event, value = window.read(timeout=10)
        if event in (None, 'Cancel'):
            break
        elif event == 'Plot':
            break
        elif event == 'Popup':
            sg.popup('Yes, your application is still running')

    window.close()


if __name__ == '__main__':
    the_gui()
