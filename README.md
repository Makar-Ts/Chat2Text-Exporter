# DiscordChannel2Text-Exporter

DiscordChannel2Text-Exporter is a Python tool that allows you to export messages from a specified Discord channel into a file. This tool can retrieve a set number of messages from a channel, or optionally all messages, and process them using custom modules.

## Features

- Export messages from a Discord channel to a markdown file.
- Define the number of messages to fetch or fetch all messages in the channel.
- Use custom processing modules for message formatting and output.
- Supports fetching messages before or after a specific message ID.
- Handles rate limiting with customizable request timeouts between message fetches.

## Requirements

- Python 3.6+
- A valid Discord Token with access to the required channel

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/your-username/DiscordChannel2Text-Exporter.git
   cd DiscordChannel2Text-Exporter
   ```

2. Configure your Discord token by editing the `config.ini` file located in the `local` directory (it will appear after the first startup automatically).

   ```ini
   [DISCORD_LOGIN]
   TOKEN=your_discord_token_here
   ```

## Usage

To run the script, use the following command:

```bash
python main.py <channel_id> <output_dir> <process_type> [options]
```

### Arguments:

- `channel_id` - The ID of the Discord channel to export messages from.
- `output_dir` - The directory where the file will be saved.
- `process_type` - The type of processing to apply to the messages (must match a module in the `process` folder).

### Options:

- `-ml`, `--messages_limit` - Limit the number of messages to fetch (default: 50).
- `-b`, `--before` - Fetch messages before this message ID.
- `-a`, `--after` - Fetch messages after this message ID.
- `-t`, `--timeout` - Set a delay between API requests in milliseconds (default: 0).
- `--all` - Fetch all messages from the channel (not recommended for large channels).

### Examples:

```bash
python main.py 1234567890 ./exports/output.md text.markdown --messages_limit 100 --before 9876543210
```

This will fetch 100 messages from channel `1234567890`, that were posted before message `9876543210`, and process them using the `markdown` processor.


```bash
python main.py 1234567890 ./exports/output json.multi --all true --timeout 1000
```

This will fetch all messages from channel `1234567890` with 1s timeout between requests, and process them using the `json.multi` processor.



## Custom Processing

The `process_type` refers to a Python module in the `process` directory. Each processor module should implement a `process_messages` function that handles the fetched messages according to your needs and help function that returns info about this processor. 

You can create custom processors by adding Python scripts to the `process` folder.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.