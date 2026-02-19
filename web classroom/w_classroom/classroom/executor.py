import subprocess
import sys
import tempfile
import os
import logging

# Get logger
logger = logging.getLogger('classroom.execution')


class CodeExecutor:
    """Execute code in different programming languages"""
    
    TIMEOUT = 10  # seconds
    
    def execute(self, code, language):
        """Execute code and return output"""
        logger.info(f"Executing {language} code (length: {len(code)} chars)")
        try:
            if language == 'python':
                result = self._execute_python(code)
            elif language == 'javascript':
                result = self._execute_javascript(code)
            elif language == 'java':
                result = self._execute_java(code)
            elif language == 'cpp':
                result = self._execute_cpp(code)
            elif language == 'c':
                result = self._execute_c(code)
            else:
                result = f"Language '{language}' is not supported yet."
                logger.warning(f"Unsupported language requested: {language}")
            
            logger.info(f"Code execution completed for {language}")
            return result
        except Exception as e:
            logger.error(f"Execution error for {language}: {e}", exc_info=True)
            return f"Execution Error: {str(e)}"
    
    def _execute_python(self, code):
        """Execute Python code"""
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            logger.debug(f"Created temporary Python file: {temp_file}")
            
            result = subprocess.run(
                [sys.executable, temp_file],
                capture_output=True,
                text=True,
                timeout=self.TIMEOUT
            )
            
            os.unlink(temp_file)
            
            output = result.stdout
            if result.stderr:
                output += "\n" + result.stderr
                if result.returncode != 0:
                    logger.warning(f"Python code executed with errors (return code: {result.returncode})")
            
            return output.strip() if output else "Code executed successfully with no output."
        except subprocess.TimeoutExpired:
            logger.warning("Python code execution timed out")
            return "Error: Code execution timed out."
        except Exception as e:
            logger.error(f"Python execution error: {e}", exc_info=True)
            return f"Error: {str(e)}"
    
    def _execute_javascript(self, code):
        """Execute JavaScript code using Node.js"""
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            result = subprocess.run(
                ['node', temp_file],
                capture_output=True,
                text=True,
                timeout=self.TIMEOUT
            )
            
            os.unlink(temp_file)
            
            output = result.stdout
            if result.stderr:
                output += "\n" + result.stderr
            
            return output.strip() if output else "Code executed successfully with no output."
        except FileNotFoundError:
            return "Error: Node.js is not installed. Please install Node.js to run JavaScript code."
        except subprocess.TimeoutExpired:
            return "Error: Code execution timed out."
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _execute_java(self, code):
        """Execute Java code"""
        try:
            # Extract class name from code
            import re
            class_match = re.search(r'public\s+class\s+(\w+)', code)
            if not class_match:
                return "Error: No public class found in Java code."
            
            class_name = class_match.group(1)
            
            with tempfile.TemporaryDirectory() as temp_dir:
                java_file = os.path.join(temp_dir, f"{class_name}.java")
                with open(java_file, 'w') as f:
                    f.write(code)
                
                # Compile
                compile_result = subprocess.run(
                    ['javac', java_file],
                    capture_output=True,
                    text=True,
                    timeout=self.TIMEOUT
                )
                
                if compile_result.returncode != 0:
                    return f"Compilation Error:\n{compile_result.stderr}"
                
                # Run
                run_result = subprocess.run(
                    ['java', '-cp', temp_dir, class_name],
                    capture_output=True,
                    text=True,
                    timeout=self.TIMEOUT
                )
                
                output = run_result.stdout
                if run_result.stderr:
                    output += "\n" + run_result.stderr
                
                return output.strip() if output else "Code executed successfully with no output."
        except FileNotFoundError:
            return "Error: Java is not installed. Please install JDK to run Java code."
        except subprocess.TimeoutExpired:
            return "Error: Code execution timed out."
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _execute_cpp(self, code):
        """Execute C++ code"""
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                source_file = os.path.join(temp_dir, 'program.cpp')
                exe_file = os.path.join(temp_dir, 'program.exe')
                
                with open(source_file, 'w') as f:
                    f.write(code)
                
                # Compile
                compile_result = subprocess.run(
                    ['g++', source_file, '-o', exe_file],
                    capture_output=True,
                    text=True,
                    timeout=self.TIMEOUT
                )
                
                if compile_result.returncode != 0:
                    return f"Compilation Error:\n{compile_result.stderr}"
                
                # Run
                run_result = subprocess.run(
                    [exe_file],
                    capture_output=True,
                    text=True,
                    timeout=self.TIMEOUT
                )
                
                output = run_result.stdout
                if run_result.stderr:
                    output += "\n" + run_result.stderr
                
                return output.strip() if output else "Code executed successfully with no output."
        except FileNotFoundError:
            return "Error: g++ is not installed. Please install MinGW or similar to compile C++ code."
        except subprocess.TimeoutExpired:
            return "Error: Code execution timed out."
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _execute_c(self, code):
        """Execute C code"""
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                source_file = os.path.join(temp_dir, 'program.c')
                exe_file = os.path.join(temp_dir, 'program.exe')
                
                with open(source_file, 'w') as f:
                    f.write(code)
                
                # Compile
                compile_result = subprocess.run(
                    ['gcc', source_file, '-o', exe_file],
                    capture_output=True,
                    text=True,
                    timeout=self.TIMEOUT
                )
                
                if compile_result.returncode != 0:
                    return f"Compilation Error:\n{compile_result.stderr}"
                
                # Run
                run_result = subprocess.run(
                    [exe_file],
                    capture_output=True,
                    text=True,
                    timeout=self.TIMEOUT
                )
                
                output = run_result.stdout
                if run_result.stderr:
                    output += "\n" + run_result.stderr
                
                return output.strip() if output else "Code executed successfully with no output."
        except FileNotFoundError:
            return "Error: gcc is not installed. Please install MinGW or similar to compile C code."
        except subprocess.TimeoutExpired:
            return "Error: Code execution timed out."
        except Exception as e:
            return f"Error: {str(e)}"
