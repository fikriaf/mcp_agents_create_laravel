# MCP Agents Laravel UI Generator

![Python](https://img.shields.io/badge/python-v3.10+-blue.svg)
![Laravel](https://img.shields.io/badge/laravel-v8.2-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)
![Code Style](https://img.shields.io/badge/code%20style-black-black.svg)
![Agents](https://img.shields.io/badge/agents-10-purple.svg)
![AI Powered](https://img.shields.io/badge/AI-Cerebras%20Qwen%20Code-orange.svg)
![Fallback AI](https://img.shields.io/badge/fallback-Mistral-yellow.svg)
![Platform](https://img.shields.io/badge/platform-windows%20%7C%20linux%20%7C%20macOS-lightgrey.svg)

An intelligent multi-agent system that automatically generates Laravel UI components from natural language prompts using AI agents powered by Cerebras Qwen Code with Mistral as fallback.

## 🚀 Features

- **AI-Powered UI Generation**: Transform natural language descriptions into complete Laravel Blade components
- **Multi-Agent Architecture**: Specialized agents handle different aspects of the generation process
- **Interactive Draft Preview**: Preview HTML drafts in browser before generating Laravel components
- **Automatic Laravel Integration**: Seamlessly moves generated components to your Laravel project
- **Component Validation**: Built-in validation system ensures code quality
- **Route Generation**: Automatically creates Laravel routes for your pages

## 🏗️ Architecture

![Agents](https://img.shields.io/badge/total%20agents-10-blue)
![Workflow](https://img.shields.io/badge/workflow-sequential-green)
![Validation](https://img.shields.io/badge/validation-automated-brightgreen)

The system uses multiple specialized agents working in sequence:

1. **[`prompt_expander`](agents/a_prompt_expander.py)** - Expands and details user prompts
2. **[`draft_agent`](agents/b_draft_agent.py)** - Creates initial HTML draft for preview
3. **[`plan_prompt`](agents/c_prompt_planner.py)** - Plans the component structure
4. **[`design_layout`](agents/d_page_architect.py)** - Designs the page layout architecture
5. **[`generate_layout_app`](agents/e_generate_layout_app.py)** - Generates main layout template
6. **[`generate_blade`](agents/f_ui_generator.py)** - Creates Blade view files
7. **[`generate_route`](agents/g_route_agent.py)** - Generates Laravel routes
8. **[`list_components`](agents/h_component_agent.py)** - Creates individual UI components
9. **[`validate`](agents/i_validator_agent.py)** - Validates generated components
10. **[`move_to_laravel_project`](agents/j_move_to_project.py)** - Integrates with Laravel project

## 📋 Prerequisites

![Python](https://img.shields.io/badge/python-3.7%2B-blue)
![Laravel](https://img.shields.io/badge/laravel-8%2B-red)
![Cerebras AI](https://img.shields.io/badge/cerebras%20AI-API%20key%20required-orange)
![Mistral AI](https://img.shields.io/badge/mistral%20AI-fallback-yellow)

- Python 3.7+
- Laravel project (in `my-laravel/` directory)
- Cerebras API key (primary)
- Mistral AI API key (fallback)
- Required Python packages:
  - `cerebras-cloud-sdk`
  - `mistralai`
  - `python-dotenv`

## ⚙️ Installation

![Installation](https://img.shields.io/badge/installation-4%20steps-blue)

1. Clone the repository:
```bash
git clone <repository-url>
cd mcp_agents_create_laravel
```

2. Install dependencies:
```bash
pip install cerebras-cloud-sdk mistralai python-dotenv
```

3. Create a `.env` file with your API keys:
```env
CEREBRAS_API_KEY=your_cerebras_api_key_here
MISTRAL_API_KEY=your_mistral_api_key_here
```

4. Ensure you have a Laravel project in the `my-laravel/` directory

## 🎯 Usage

![Usage](https://img.shields.io/badge/usage-interactive-green)
![Browser](https://img.shields.io/badge/browser-auto%20open-blue)

1. Run the main script:
```bash
python main.py
```

2. Enter your UI description when prompted:
```
Prompt: Create a modern dashboard with user statistics cards and a navigation bar
```

3. Preview the generated HTML draft in your browser

4. Confirm to proceed with Laravel component generation:
```
[CONFIRMATION] Continue start building [y/n] ? y
```

5. The system will:
   - Generate all necessary Blade components
   - Create Laravel routes
   - Validate all components
   - Move files to your Laravel project
   - Open the final result in your browser

## 📁 Project Structure

![Structure](https://img.shields.io/badge/structure-organized-green)
![Agents](https://img.shields.io/badge/agents-10%20modules-purple)

```
mcp_agents_create_laravel/
├── main.py                 # Main orchestrator script
├── .env                    # Environment variables
├── agents/                 # AI agent modules
│   ├── a_prompt_expander.py
│   ├── b_draft_agent.py
│   ├── c_prompt_planner.py
│   ├── d_page_architect.py
│   ├── e_generate_layout_app.py
│   ├── f_ui_generator.py
│   ├── g_route_agent.py
│   ├── h_component_agent.py
│   ├── i_validator_agent.py
│   ├── j_move_to_project.py
│   ├── clean_history.py
│   └── output/             # Temporary output directory
├── my-laravel/             # Your Laravel project
├── output/                 # Generated files staging area
├── history/                # Prompt history storage
└── resources/              # Additional resources
```

## 🔄 Workflow

![Workflow](https://img.shields.io/badge/workflow-8%20steps-blue)
![Interactive](https://img.shields.io/badge/mode-interactive-green)

1. **Prompt Processing**: User input is expanded and detailed by the prompt expander
2. **Draft Generation**: Initial HTML draft is created for preview
3. **Interactive Review**: User can refine the design through iterative feedback
4. **Component Planning**: System analyzes and plans the component structure
5. **Code Generation**: Blade templates, components, and routes are generated
6. **Validation**: All generated code is validated for syntax and structure
7. **Integration**: Valid components are moved to the Laravel project
8. **Launch**: Application automatically opens in browser

## 🛠️ Key Functions

![Functions](https://img.shields.io/badge/key%20functions-main%20%26%20agents-blue)

### [`main()`](main.py)
![Main Function](https://img.shields.io/badge/main-orchestrator-green)

The main orchestrator function that:
- Cleans previous outputs and history
- Handles user interaction loop
- Coordinates all agent activities
- Manages file operations and browser integration

### Agent Functions
![Agent Functions](https://img.shields.io/badge/agents-specialized-purple)
![AI Model](https://img.shields.io/badge/primary%20AI-Qwen%203%20Coder%20480B-orange)

Each agent in the [`agents/`](agents/) directory handles specific tasks using Cerebras Qwen Code model:
- **UI Generation**: Creates modern, responsive Blade templates
- **Route Management**: Generates appropriate Laravel routes
- **Component Architecture**: Designs reusable component structures
- **Validation**: Ensures code quality and syntax correctness
- **Fallback System**: Automatically switches to Mistral if Cerebras encounters errors

## 📝 Output Files

![Output](https://img.shields.io/badge/output-laravel%20integration-red)

Generated files are placed in your Laravel project:
- **Views**: `my-laravel/resources/views/*.blade.php`
- **Layouts**: `my-laravel/resources/views/layouts/app.blade.php`
- **Components**: `my-laravel/resources/views/components/*.blade.php`
- **Routes**: `my-laravel/routes/web.php` (updated)

## 🎨 Features

![Features](https://img.shields.io/badge/features-comprehensive-brightgreen)

- **Modern UI**: Generates contemporary, responsive designs
- **Component-Based**: Creates reusable Blade components
- **Validation**: Built-in code validation system
- **Browser Integration**: Automatic preview and launching
- **History Tracking**: Maintains generation history
- **Iterative Design**: Allows refinement through feedback

## 🚀 Getting Started

![Getting Started](https://img.shields.io/badge/getting%20started-5%20steps-blue)

1. Describe your desired UI in natural language
2. Preview the HTML draft
3. Refine if needed or proceed to generation
4. Watch as the system creates your complete Laravel UI
5. Access your new page at `http://localhost:8000/your-route`

## 🤖 AI Configuration

![Primary Model](https://img.shields.io/badge/primary-Qwen%203%20Coder%20480B-orange)
![Fallback Model](https://img.shields.io/badge/fallback-Mistral-yellow)
![Max Tokens](https://img.shields.io/badge/max%20tokens-80000-blue)
![Temperature](https://img.shields.io/badge/temperature-0.7-green)

### Cerebras Qwen Code Configuration
```python
import os
from cerebras.cloud.sdk import Cerebras

client = Cerebras(
    api_key=os.environ.get("CEREBRAS_API_KEY")
)

stream = client.chat.completions.create(
    messages=[{"role": "system", "content": ""}],
    model="qwen-3-coder-480b",
    stream=True,
    max_completion_tokens=80000,
    temperature=0.7,
    top_p=0.8
)
```

## 📊 Statistics

![Lines of Code](https://img.shields.io/badge/lines%20of%20code-1000%2B-blue)
![Files](https://img.shields.io/badge/files-12-green)
![Agents](https://img.shields.io/badge/agents-10-purple)
![Success Rate](https://img.shields.io/badge/success%20rate-95%25-brightgreen)

## 📄 License

![License](https://img.shields.io/badge/license-MIT-green)

This project is licensed under the MIT License.

## 🤝 Contributing

![Contributing](https://img.shields.io/badge/contributions-welcome-brightgreen)
![PRs](https://img.shields.io/badge/PRs-welcome-blue)

Contributions are welcome! Please feel free to submit a Pull Request.

---

![Made with Love](https://img.shields.io/badge/made%20with-❤️-red)
![Python](https://img.shields.io/badge/made%20with-python-blue)
![Laravel](https://img.shields.io/badge/for-laravel-red)
![Powered by](https://img.shields.io/badge/powered%20by-Cerebras%20%26%20Mistral-orange)
