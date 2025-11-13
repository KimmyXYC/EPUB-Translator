# EPUB Translator GUI Description

## Main Window

The GUI provides an intuitive interface for translating EPUB files:

### Layout

```
┌────────────────────────────────────────────────────────────────┐
│  EPUB Translator                                          [_][□][X]│
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  API Configuration                                             │
│  ─────────────────────────────────────────────────────────    │
│                                                                │
│  API Key:         [••••••••••••••••••••••••••••••••••••••]    │
│                                                                │
│  API Base URL:    [https://api.openai.com/v1            ]    │
│                                                                │
│                                                                │
│  Translation Settings                                          │
│  ─────────────────────────────────────────────────────────    │
│                                                                │
│  Source Language: [auto ▼]                                    │
│                                                                │
│  Target Language: [zh   ▼]                                    │
│                                                                │
│                                                                │
│  File Selection                                                │
│  ─────────────────────────────────────────────────────────    │
│                                                                │
│  Input EPUB:      No file selected         [Browse...]        │
│                                                                │
│  Output EPUB:     No file selected         [Browse...]        │
│                                                                │
│  ──────────────────────────────────────────────────────────  │
│  [████████████████████████░░░░░░░░░░░░░░░░░] 45%             │
│                                                                │
│  Ready                                                         │
│                                                                │
│                       [Translate]                              │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

## Features

### 1. API Configuration Section
- **API Key**: Secure password-masked input field for OpenAI or compatible API key
- **API Base URL**: Configurable endpoint URL (defaults to OpenAI, but can use compatible APIs)

### 2. Translation Settings Section
- **Source Language**: Dropdown menu with options:
  - auto (Auto-detect)
  - en (English)
  - ja (Japanese)
  - ko (Korean)
  - zh (Chinese)
  - es (Spanish)
  - fr (French)
  - de (German)
  - ru (Russian)

- **Target Language**: Dropdown menu with same options as source (excluding auto)

### 3. File Selection Section
- **Input EPUB**: 
  - Label shows selected filename or "No file selected"
  - Browse button opens file picker for .epub files
  
- **Output EPUB**:
  - Label shows output filename or "No file selected"
  - Browse button opens save dialog
  - Auto-suggests filename based on input (e.g., `book.epub` → `book_translated.epub`)

### 4. Progress Section
- **Progress Bar**: Animated progress indicator showing translation progress
- **Status Label**: Shows current status:
  - "Ready" (blue) - Initial state
  - "Translating..." (blue) - During translation
  - "Translation completed successfully!" (green) - On success
  - "Translation failed" (red) - On error

### 5. Action Button
- **Translate Button**: 
  - Starts the translation process
  - Disabled during translation to prevent multiple simultaneous translations
  - Re-enabled after completion

## User Workflow

1. **Enter API credentials**
   - Input your OpenAI API key or compatible service key
   - Optionally modify the API base URL for custom endpoints

2. **Configure languages**
   - Select source language (or use auto-detect)
   - Select target language

3. **Select files**
   - Click "Browse..." for Input EPUB
   - Navigate to and select your EPUB file
   - Output location is auto-suggested, or click "Browse..." to choose custom location

4. **Start translation**
   - Click "Translate" button
   - Watch progress bar for status
   - Wait for completion message

5. **Result**
   - Success: Dialog shows "Translation completed!" with output file location
   - Failure: Error dialog with details

## Technical Details

- Built with Python's tkinter for cross-platform compatibility
- Non-blocking translation using threading to keep UI responsive
- Progress callbacks update UI in real-time
- Form validation before starting translation
- Error handling with user-friendly messages

## Benefits

- **User-Friendly**: No command-line knowledge required
- **Visual Feedback**: Progress bar and status updates
- **Flexible**: Works with OpenAI and compatible APIs
- **Safe**: Input validation and error handling
- **Convenient**: Auto-suggests output filenames
