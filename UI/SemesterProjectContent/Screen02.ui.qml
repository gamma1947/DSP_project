/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/

import QtQuick
import QtQuick.Controls
import QtGraphs

Rectangle {
    id: screen2
    width: 1920
    height: 1080
    color: "#58f5c6"

    Image {
        id: image
        x: -285
        y: -130
        width: 2473
        height: 1327
        source: "images/view-metro-city-buildings-cityscape.jpg"
        fillMode: Image.PreserveAspectFit
    }

    Rectangle {
        id: rectangle
        x: 0
        y: 0
        width: 100
        height: 1080
        opacity: 0.3
        color: "#c1e9f9"
        border.color: "#ffffff"
    }

    Button {
        id: button
        x: 1655
        y: 121
        width: 150
        height: 55
        text: qsTr("Fetch Data")
    }

    Text {
        id: text1
        x: 200
        y: 50
        width: 836
        height: 83
        text: qsTr("Urban Air Quality Monitoring dashboard")
        font.pixelSize: 40
        font.styleName: "Regular"
        font.family: "Verdana"
    }

    Rectangle {
        id: rectangle1
        x: 200
        y: 122
        width: 293
        height: 55
        opacity: 0.5
        color: "#ffffff"
        bottomRightRadius: 10
        bottomLeftRadius: 10
        topRightRadius: 10
        topLeftRadius: 10

        ComboBox {
            id: comboBox
            x: 100
            y: 8
            width: 171
            height: 40
            focusPolicy: Qt.StrongFocus
            font.pointSize: 10
            currentIndex: 1
            displayText: "Pune"
            textRole: "City"
        }

        Text {
            id: text2
            x: 31
            y: 14
            width: 38
            height: 28
            text: qsTr("City : ")
            font.pixelSize: 20
            transformOrigin: Item.Center
        }
    }

    Rectangle {
        id: rectangle2
        x: 530
        y: 122
        width: 291
        height: 55
        opacity: 0.5
        color: "#ffffff"
        topRightRadius: 10
        topLeftRadius: 10
        ComboBox {
            id: comboBox1
            x: 115
            y: 8
            width: 159
            height: 40
            textRole: "City"
            font.pointSize: 10
            focusPolicy: Qt.StrongFocus
            displayText: "CBP"
            currentIndex: 1
        }

        Text {
            id: text3
            x: 31
            y: 14
            width: 38
            height: 28
            text: qsTr("Source :")
            font.pixelSize: 20
            transformOrigin: Item.Center
        }
        bottomRightRadius: 10
        bottomLeftRadius: 10
    }

    Rectangle {
        id: rectangle3
        x: 858
        y: 122
        width: 304
        height: 55
        opacity: 0.5
        color: "#ffffff"
        topRightRadius: 10
        topLeftRadius: 10
        ComboBox {
            id: comboBox2
            x: 128
            y: 8
            width: 160
            height: 40
            textRole: "City"
            font.pointSize: 10
            focusPolicy: Qt.StrongFocus
            displayText: "PM 2.5"
            currentIndex: 1
        }

        Text {
            id: text4
            x: 31
            y: 14
            width: 38
            height: 28
            text: qsTr("Pollutant :")
            font.pixelSize: 20
            transformOrigin: Item.Center
        }
        bottomRightRadius: 10
        bottomLeftRadius: 10
    }

    Rectangle {
        id: rectangle4
        x: 1201
        y: 122
        width: 400
        height: 55
        opacity: 0.5
        color: "#ffffff"
        topRightRadius: 10
        topLeftRadius: 10
        ComboBox {
            id: comboBox3
            x: 100
            y: 8
            width: 280
            height: 40
            textRole: "City"
            font.pointSize: 10
            focusPolicy: Qt.StrongFocus
            displayText: "Apr 1, 2024 - Apr 1, 2025"
            currentIndex: 1
        }

        Text {
            id: text5
            x: 31
            y: 14
            width: 38
            height: 28
            text: qsTr("Date :")
            font.pixelSize: 20
            transformOrigin: Item.Center
        }
        bottomRightRadius: 10
        bottomLeftRadius: 10
    }

    Rectangle {
        id: rectangle5
        x: 200
        y: 220
        width: 370
        height: 150
        opacity: 0.4
        color: "#ffffff"
        bottomRightRadius: 20
        bottomLeftRadius: 20
        topRightRadius: 20
        topLeftRadius: 20
    }

    Rectangle {
        id: rectangle6
        x: 610
        y: 220
        width: 370
        height: 150
        opacity: 0.4
        color: "#ffffff"
        topRightRadius: 20
        topLeftRadius: 20
        bottomRightRadius: 20
        bottomLeftRadius: 20
    }

    Rectangle {
        id: rectangle7
        x: 1020
        y: 220
        width: 370
        height: 150
        opacity: 0.4
        color: "#ffffff"
        topRightRadius: 20
        topLeftRadius: 20
        bottomRightRadius: 20
        bottomLeftRadius: 20
    }

    Rectangle {
        id: rectangle8
        x: 1430
        y: 220
        width: 370
        height: 150
        opacity: 0.4
        color: "#ffffff"
        topRightRadius: 20
        topLeftRadius: 20
        bottomRightRadius: 20
        bottomLeftRadius: 20
    }

    Switch {
        id: switch1
        x: 1046
        y: 489
        text: qsTr("Realtime")
    }

    GraphsView {
        id: area
        x: 200
        y: 451
        width: 980
        height: 503
        opacity: 0.8
        marginTop: 100
        marginBottom: 100
        ValueAxis {
            id: valueAxisX
            min: 0
            max: 10
        }

        ValueAxis {
            id: valueAxisY
            min: 0
            max: 10
        }

        AreaSeries {
            name: "AreaSeries"
            upperSeries: lineSeries
            LineSeries {
                id: lineSeries
                XYPoint {
                    x: 0
                    y: 1.5
                }

                XYPoint {
                    x: 1
                    y: 3
                }

                XYPoint {
                    x: 6
                    y: 6.3
                }

                XYPoint {
                    x: 10
                    y: 3.1
                }
            }
        }


        axisY: valueAxisY
        axisX: valueAxisX
    }

    Rectangle {
        id: rectangle9
        x: 1280
        y: 451
        width: 525
        height: 503
        opacity: 0.4
        color: "#ffffff"
        topRightRadius: 20
        topLeftRadius: 20
        bottomRightRadius: 20
        bottomLeftRadius: 20
    }

    Text {
        id: text6
        x: 1305
        y: 470
        text: qsTr("Recent Alerts")
        font.pixelSize: 30
    }

    Text {
        id: text7
        x: 240
        y: 470
        text: qsTr("PM 2.5 Levels over Time")
        font.pixelSize: 30
    }

    Text {
        id: text8
        x: 276
        y: 240
        color: "#177b28"
        text: qsTr("Current P.M. 2.5")
        font.pixelSize: 20
    }

    Text {
        id: text9
        x: 276
        y: 271
        color: "#000000"
        text: qsTr("118 mu/m3")
        font.pixelSize: 20
    }




}
