This is the standard ninja.exe with an embedded manifest to support long file names.

To embed this manifest:

    1) Create the file 'ninja.exe.manifest' along side 'ninja.exe' with the contents:

        <?xml version='1.0' encoding='UTF-8' standalone='yes'?>
        <assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0" xmlns:asmv3="urn:schemas-microsoft-com:asm.v3" >
            <application xmlns="urn:schemas-microsoft-com:asm.v3">
                <windowsSettings xmlns:ws2="http://schemas.microsoft.com/SMI/2016/WindowsSettings">
                    <ws2:longPathAware>true</ws2:longPathAware>
                </windowsSettings>
            </application>
        </assembly>

    2) Run the command:

        mt.exe -manifest ninja.exe.manifest -outputresource:"ninja.exe;1"
