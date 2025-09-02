#!/bin/bash
echo "📝 Adding New Review..."

# Run markdown converter
cd python_backend && source venv/bin/activate && python markdown_converter.py

echo "✅ Review processed!"
echo "🚀 Ready to deploy: git add . && git commit -m 'Add new review' && git push"
