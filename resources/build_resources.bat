echo "building user interfaces..."
pyside-uic -o ../python/tk_multi_renderfarm/ui/dialog.py dialog.ui
pyside-uic -o ../python/tk_multi_renderfarm/ui/output_item.py output_item.ui
echo "building resources..."
pyside-rcc -o ../python/tk_multi_renderfarm/ui/resources_rc.py resources.qrc