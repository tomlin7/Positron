#!/usr/bin/env node

import { Command } from 'commander';
import prompts from 'prompts';
import chalk from 'chalk';
import fs from 'fs-extra';
import path from 'path';
import { fileURLToPath } from 'url';
import ora from 'ora';

const program = new Command();
const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Main CLI execution
async function main() {
    console.log('\n');
    console.log(chalk.bold.white('  POSITRON'));
    console.log(chalk.gray('  Desktop App Initializer'));
    console.log('\n');

    // Define CLI metadata
    program
        .name('create-positron-app')
        .description('CLI to bootstrap Positron apps')
        .version('0.1.0')
        .argument('[project-name]', 'Name of the project directory')
        .option('-t, --template <template-name>', 'Specify the template to use (react-app, vue-app, svelte-app, nextjs-app, vanilla-app)')
        .action(async (projectName, options) => {
            let targetDir = projectName;

            // Prompt for project name if not provided
            if (!targetDir) {
                const response = await prompts({
                    type: 'text',
                    name: 'projectName',
                    message: chalk.white('What is your project named?'),
                    initial: 'my-positron-app',
                    format: v => v
                });
                targetDir = response.projectName;
            }

            if (!targetDir) {
                console.log(chalk.red('Project name is required.'));
                process.exit(1);
            }

            let template = options.template;

            // Prompt for template if not provided via flag
            if (!template) {
                const templateResponse = await prompts({
                    type: 'select',
                    name: 'template',
                    message: chalk.white('Which template would you like to use?'),
                    choices: [
                        { title: 'React', value: 'react-app' },
                        { title: 'Vue', value: 'vue-app' },
                        { title: 'Svelte', value: 'svelte-app' },
                        { title: 'Next.js', value: 'nextjs-app' },
                        { title: 'Vanilla', value: 'vanilla-app' }
                    ],
                    initial: 0
                });
                template = templateResponse.template;
            }

            if (!template) {
                console.log(chalk.red('Template selection is required.'));
                process.exit(1);
            }

            const projectPath = path.resolve(process.cwd(), targetDir);

            const spinner = ora(chalk.gray('Copying template files...')).start();

            try {
                const scriptDir = path.dirname(fileURLToPath(import.meta.url));
                const templateDir = path.resolve(scriptDir, 'templates', template);

                if (!fs.existsSync(templateDir)) {
                    spinner.fail(`Template directory not found at ${templateDir}`);
                    process.exit(1);
                }

                // Filter out node_modules, .git, and dist
                const filterFunc = (src, dest) => {
                    const basename = path.basename(src);
                    if (basename === 'node_modules') return false;
                    if (basename === 'dist') return false;
                    if (basename === '.git') return false;
                    if (basename === '.DS_Store') return false;
                    return true;
                };

                await fs.copy(templateDir, projectPath, { filter: filterFunc });

                // Update package.json name
                const pkgJsonPath = path.join(projectPath, 'package.json');
                if (fs.existsSync(pkgJsonPath)) {
                    const pkg = await fs.readJson(pkgJsonPath);
                    pkg.name = targetDir;
                    await fs.writeJson(pkgJsonPath, pkg, { spaces: 2 });
                }

                spinner.succeed(chalk.white('Template copied successfully.'));

                console.log('\n');
                console.log(chalk.gray('  01. ') + chalk.white('cd ') + chalk.white(targetDir));
                console.log(chalk.gray('  02. ') + chalk.white('npm install'));
                console.log(chalk.gray('  03. ') + chalk.white('npm run dev'));
                console.log('\n');

            } catch (err) {
                spinner.fail('Failed to copy template files.');
                console.error(err);
                process.exit(1);
            }

        });

    program.parse(process.argv);
}

main().catch((err) => {
    console.error(err);
    process.exit(1);
});
