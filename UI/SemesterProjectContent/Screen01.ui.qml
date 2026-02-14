

/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/
import QtQuick
import QtQuick.Controls
import SemesterProject
import QtQuick.Studio.Components
import QtQuick.Studio.DesignEffects

Rectangle {
    width: Constants.width
    height: Constants.height

    color: Constants.backgroundColor
    activeFocusOnTab: true

    Image {
        id: image1
        x: -285
        y: -130
        width: 2473
        height: 1327
        source: "images/view-metro-city-buildings-cityscape.jpg"
        fillMode: Image.PreserveAspectFit
    }
    Rectangle {
        id: rectangle
        x: 127
        y: 98
        width: 1675
        height: 892
        opacity: 0.2
        color: "#ffffff"
        bottomRightRadius: 30
        topRightRadius: 30
        bottomLeftRadius: 30
        topLeftRadius: 30

        RectangleItem {
            id: rectangle1
            x: 1087
            y: 326
            width: 450
            height: 240
            opacity: 0.5
            strokeColor: "#e0e0e0"
            adjustBorderRadius: true
        }
    }
    TextField {
        id: textField1
        x: 1241
        y: 559
        width: 400
        height: 60
        text: ""
        placeholderText: "Password"
    }

    TextField {
        id: textField
        x: 1241
        y: 471
        width: 400
        height: 60
        text: ""
        placeholderText: qsTr("Login Id")
    }

    Text {
        id: text1
        x: 255
        y: 239
        width: 834
        height: 106
        color: "#2e7d32"
        text: qsTr("Urban Air Quality Dashboard")
        font.pixelSize: 50
        font.styleName: "Bold"
        font.family: "Verdana"
    }

    Button {
        id: button
        x: 1217
        y: 704
        width: 448

        height: 80
        text: qsTr("Sign in")
        layer.enabled: false
        icon.color: "#dd0c0c0c"
        highlighted: false
        checkable: true
        font.bold: true
        font.pointSize: 20
    }
}
