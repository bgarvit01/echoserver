"""
File operation utilities with security controls and error handling.
"""

import os
import json
from pathlib import Path
from typing import Optional, List


class FileManager:
    """Handles file operations with security controls."""
    
    # Allowed paths for security (can be configured)
    ALLOWED_PREFIXES = ['/tmp', '/app', '/var/tmp']
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB limit
    
    def __init__(self, allowed_prefixes: Optional[List[str]] = None):
        """Initialize FileManager with optional custom allowed prefixes."""
        if allowed_prefixes is not None:
            self.allowed_prefixes = allowed_prefixes
        else:
            self.allowed_prefixes = self.ALLOWED_PREFIXES.copy()
    
    def read_file_or_directory(self, path: str) -> str:
        """
        Read file content or list directory contents with security checks.
        
        Args:
            path: File or directory path to read
            
        Returns:
            JSON string with content or error message
        """
        try:
            # Security validation
            if not self._is_path_allowed(path):
                return json.dumps({"error": "Access denied - path not allowed"})
            
            resolved_path = Path(path).resolve()
            
            if resolved_path.is_dir():
                return self._list_directory(resolved_path)
            elif resolved_path.is_file():
                return self._read_file(resolved_path)
            else:
                return json.dumps({"error": "File or directory not found"})
                
        except PermissionError:
            return json.dumps({"error": "Permission denied"})
        except OSError as e:
            return json.dumps({"error": f"OS error: {str(e)}"})
        except Exception as e:
            return json.dumps({"error": f"Unexpected error: {str(e)}"})
    
    def _is_path_allowed(self, path: str) -> bool:
        """
        Check if the path is allowed based on security rules.
        
        Args:
            path: Path to validate
            
        Returns:
            True if path is allowed, False otherwise
        """
        # Prevent path traversal attacks
        if '..' in path:
            return False
        
        # For absolute paths, check against allowed prefixes
        if os.path.isabs(path):
            return any(path.startswith(prefix) for prefix in self.allowed_prefixes)
        
        # Relative paths are generally allowed but be cautious
        # You might want to restrict this further based on your security needs
        return not path.startswith('/')
    
    def _list_directory(self, directory_path: Path) -> str:
        """
        List directory contents and return as JSON.
        
        Args:
            directory_path: Path object for directory
            
        Returns:
            JSON string with sorted list of entries
        """
        try:
            entries = []
            for entry in directory_path.iterdir():
                entry_info = {
                    "name": entry.name,
                    "type": "directory" if entry.is_dir() else "file"
                }
                
                # Add size for files (safely)
                if entry.is_file():
                    try:
                        stat = entry.stat()
                        entry_info["size"] = stat.st_size
                        entry_info["modified"] = stat.st_mtime
                    except (OSError, PermissionError):
                        # If we can't get stats, just include name and type
                        pass
                
                entries.append(entry_info)
            
            # Sort by name
            entries.sort(key=lambda x: x["name"].lower())
            return json.dumps(entries, indent=2)
            
        except PermissionError:
            return json.dumps({"error": "Permission denied reading directory"})
        except Exception as e:
            return json.dumps({"error": f"Error listing directory: {str(e)}"})
    
    def _read_file(self, file_path: Path) -> str:
        """
        Read file content with size and encoding checks.
        
        Args:
            file_path: Path object for file
            
        Returns:
            File content as string
        """
        try:
            # Check file size
            file_size = file_path.stat().st_size
            if file_size > self.MAX_FILE_SIZE:
                return json.dumps({
                    "error": f"File too large ({file_size} bytes), maximum allowed: {self.MAX_FILE_SIZE}"
                })
            
            # Try to read as text with common encodings
            encodings = ['utf-8', 'utf-16', 'iso-8859-1', 'cp1252']
            
            for encoding in encodings:
                try:
                    with file_path.open('r', encoding=encoding) as f:
                        return f.read()
                except UnicodeDecodeError:
                    continue
            
            # If all text encodings fail, treat as binary and return info
            return json.dumps({
                "error": "Binary file detected",
                "info": {
                    "size": file_size,
                    "name": file_path.name,
                    "type": "binary"
                }
            })
            
        except PermissionError:
            return json.dumps({"error": "Permission denied reading file"})
        except Exception as e:
            return json.dumps({"error": f"Error reading file: {str(e)}"})
    
    def add_allowed_prefix(self, prefix: str) -> None:
        """Add an allowed path prefix for security."""
        if prefix not in self.allowed_prefixes:
            self.allowed_prefixes.append(prefix)
    
    def remove_allowed_prefix(self, prefix: str) -> None:
        """Remove an allowed path prefix."""
        if prefix in self.allowed_prefixes:
            self.allowed_prefixes.remove(prefix)
    
    def get_allowed_prefixes(self) -> List[str]:
        """Get current list of allowed path prefixes."""
        return self.allowed_prefixes.copy()
