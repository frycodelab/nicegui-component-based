from nicegui import ui, app
from io import BytesIO
import base64
import asyncio

def content(data) -> None:

    def base64_decode(base64_string):
        """
        Decodes a Base64 string to its original representation.

        Args:
            base64_string: The Base64 encoded string.

        Returns:
            str: The decoded string.
        """
        try:
            # Decode the Base64 string to bytes
            decoded_bytes = base64.b64decode(base64_string) 

            # Decode the bytes to a string (assuming UTF-8 encoding)
            decoded_string = decoded_bytes.decode('utf-8') 

            return decoded_string
        except Exception as e:
            print(f"Error decoding Base64 string: {e}")
            return None
    decoded_data = base64_decode(data)
    
    ui.html(
        f'''
        <div id="print"> {decoded_data} </div>
        ''')
    
    ui.run_javascript('''

        function printWithoutBlocking() {
        // Create an invisible iframe
        const iframe = document.createElement('iframe');
        iframe.style.position = 'absolute';
        iframe.style.width = '0';
        iframe.style.height = '0';
        iframe.style.border = 'none';
        document.body.appendChild(iframe);

        // Get the iframe's document and copy the current tab's content
        const iframeDoc = iframe.contentWindow.document;
        iframeDoc.open();
        iframeDoc.write(document.documentElement.outerHTML);
        iframeDoc.close();

        // Trigger printing from the iframe
        iframe.contentWindow.focus();
        iframe.contentWindow.print();

        // Remove the iframe after a delay to ensure the printing process completes
        document.body.removeChild(iframe);
        window.close();
        }

        // Example usage:
        printWithoutBlocking();
                                                      
        ''')
    #ui.run_javascript('window.print();')    
    