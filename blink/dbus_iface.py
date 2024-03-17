import sdbus


class Blink(
    sdbus.DbusInterfaceCommonAsync,
    interface_name='me.faschingbauer.Blink'
):
    @sdbus.dbus_method_async(
        result_signature='as',
    )
    async def Programs(self):
        return ['blah', 'blech']
