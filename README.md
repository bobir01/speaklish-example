README SpeaklishClient:

---

# SpeaklishClient

## Overview
SpeaklishClient is a Python class designed to interact with the Speaklish API for conducting language tests. It simplifies the process of creating sessions, sending test answers, and retrieving feedback.

## Prerequisites
- Python 3.x
- `requests` library (`pip install requests`)
- `python-dotenv` library for env files
- `.env` file containing the necessary environment variables

## Usage
1. **Installation**: Copy the `SpeaklishClient` class into your project directory or import it directly.

2. **Setup**:
   - Ensure you have the required environment variables set in a `.env` file (e.g., `DJANGO_SUPERUSER_USERNAME` and `DJANGO_SUPERUSER_PASSWORD`).
   - Modify the base directory (`BASE_DIR`) in the `SpeaklishClient` class if your project structure differs.

3. **Usage**:
   ```python
   from speaklish_client import SpeaklishClient

   # Create an instance of the SpeaklishClient
   client = SpeaklishClient()

   # Run the test
   client.run_test()
   ```

4. **Test Execution**:
   - Upon running `run_test()`, the client will:
     - Create a session.
     - Send answers for part 1 and part 3 questions.
     - Send the answer for the part 2 question.
     - Wait for feedback for 30 seconds.
     - Print the feedback received.

## Notes
- Ensure that the audio files referenced in the code exist in the specified directory that comes with its own repo
- This client is tailored specifically for the Speaklish API and may require modifications for use with other APIs.

## Support
For any questions, issues, or feedback, please contact [bob@speaklish.uz].
