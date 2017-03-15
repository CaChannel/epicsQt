
style = \
    """
    QWidget:disabled{
                border-width:3px;
                border-color:white;
                color:white;
                background-color:white;
    }

    QLineEdit:focus{
                border-style:solid;
                border-color:black;
                border-width:2px;
                background-color:lightgreen;
    }

    QLineEdit:enabled{
                color:black;
                background-color:lightgreen;
    }


    QLabel:enabled{
                border-width:1px;
                color:black;
                background-color:lightgreen;
    }

    """
normal = "color:black;background-color:lightgreen;"

warn = "color:black;background-color:yellow;"

alarm = "color:black;background-color:red;"

invalid = normal
# invalid = "border-style:solid;border-width:1px;border-color:white;"

disabled = "border-style:solid;border-width:5px;border-color:white;color:white;background-color:white;"
