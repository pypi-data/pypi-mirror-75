import PySimpleGUI as sg
from multiprocessing import Process


def dialog(title, text, block=True):
    if not block:
        Process(target=dialog, args=(title, text)).start()
        return
    window = sg.Window(title, [
        [sg.Text(text)],
        [sg.Button('OK')]
    ])
    window.read()
    window.close()


def confirm(title, text, **kwargs):
    if 'yesno' in kwargs.keys() and kwargs['yesno']:
        yes = 'Yes'
        no = 'No'
    else:
        yes = kwargs['yes'] if 'yes' in kwargs.keys() else 'OK'
        no = kwargs['no'] if 'no' in kwargs.keys() else 'Cancel'
    window = sg.Window(title, [
        [sg.Text(text)],
        [sg.Button(yes), sg.Button(no)]
    ])

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            return False
        elif event == yes:
            window.close()
            return True
        elif event == no:
            window.close()
            return False


def text(title, text, canCancel=True, yes='OK', no='Cancel', password=False, validate=None):
    while True:
        window = sg.Window(title, [
            [sg.Text(text)],
            [sg.InputText(password_char='*' if password else '')],
            ([sg.Button(yes), sg.Button(no)] if canCancel else[sg.Button(yes)])
        ])

        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                return None
            elif event == yes:
                window.close()
                if validate == None:
                    return values[0]
                elif validate(values[0]):
                    return values[0]
                else:
                    break
            elif event == no:
                window.close()
                return None


def choice(title, text, choices, canCancel=True, no='Cancel'):
    windowItems = [[sg.Text(text)]]
    for choice in choices:
        windowItems.append([sg.Button(str(choice))])
    if canCancel:
        windowItems.append([sg.Button(no)])
    window = sg.Window(title, windowItems)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            return None
        elif event == no:
            window.close()
            return None
        elif event in choices:
            window.close()
            return event


def choiceMulti(title, text, choices, canCancel=True, yes='Done', no='Cancel'):
    windowItems = [[sg.Text(text)]]
    for choice in choices:
        windowItems.append([sg.Checkbox(str(choice))])
    if canCancel:
        windowItems.append([sg.Button(yes), sg.Button(no)])
    else:
        windowItems.append([sg.Button(yes)])
    window = sg.Window(title, windowItems)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            return None
        elif event == no:
            window.close()
            return None
        elif event == yes:
            window.close()
            result = []
            for i in range(len(values)):
                if values[i]:
                    result.append(choices[i])
            return result
