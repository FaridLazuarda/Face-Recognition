int main(int argc, char *argv[]) {
    QApplication a(argc, argv);
    QLabel label("<img src='image.jpg' />");
    label.show();
    return a.exec();
}

