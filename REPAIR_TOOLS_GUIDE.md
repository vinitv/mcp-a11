# 🔧 Home Repair Cost Estimation Tools

This MCP server now includes comprehensive tools for getting home repair cost estimates through integration with the Repair Cost API.

## 🛠️ Available Tools

### 1. `get_repair_cost`
Get detailed cost estimates for specific repair types.

**Usage:**
- `repair_type`: Type of repair (e.g., "electrical_panel_replacement", "roof_leak_repair")
- `zip_code`: 5-digit zip code for location-based pricing
- `scope`: "minimal", "average", or "comprehensive" (default: "average")

**Example:** *"What's the cost to replace an electrical panel in 10001?"*

### 2. `list_repair_types`
Browse all available repair types with descriptions and cost ranges.

**Usage:**
- `category`: Optional filter by category (e.g., "Electrical", "Plumbing", "HVAC")

**Example:** *"Show me all electrical repair types"*

### 3. `get_batch_repair_costs`
Get cost estimates for multiple repairs at once (up to 10).

**Usage:**
- `repair_types`: Comma-separated list of repair types
- `zip_code`: 5-digit zip code
- `scope`: "minimal", "average", or "comprehensive" (default: "average")

**Example:** *"What would it cost to replace electrical panel and fix roof leak in 90210?"*

## 🎯 Sample Questions You Can Ask

1. **Single Repair Cost:**
   - "How much does electrical panel replacement cost in 90210?"
   - "What's the price range for roof leak repair in New York?"

2. **Browse Available Repairs:**
   - "What electrical repairs are available?"
   - "Show me all plumbing repair types"
   - "List all available home repairs"

3. **Multiple Repairs:**
   - "Get costs for electrical_panel_replacement, roof_leak_repair in 10001"
   - "How much for comprehensive electrical rewiring and HVAC installation in 90210?"

## 📊 What You Get

Each estimate includes:
- **Cost Range**: Low, average, and high estimates
- **Regional Pricing**: Location-based adjustments
- **Labor Details**: Estimated hours and complexity
- **Materials**: Cost percentage breakdown
- **Permits**: Whether permits are required
- **Urgency Level**: How critical the repair is
- **Cost Factors**: Regional labor costs, material availability, permit complexity

## 🔑 Technical Details

- **API Configuration**: Stored securely in `.env` file
- **Environment Variables**: 
  - `REPAIR_API_BASE_URL`: API endpoint URL
  - `REPAIR_API_KEY`: Your API key for authentication
- **Rate Limits**: 1000 requests per day
- **Regional Support**: US zip codes with regional cost adjustments
- **Categories**: Electrical, Plumbing, HVAC, Roofing, Foundation, Flooring, Painting, Windows, Doors, Insulation

## 🚀 Setup

1. **Environment Configuration**: 
   - Copy `.env.sample` to `.env` if you haven't already
   - Set your `REPAIR_API_KEY` in the `.env` file
   - The API base URL is pre-configured

2. **Getting an API Key**:
   ```bash
   curl -X POST "https://repair-cost-api-618596951812.us-central1.run.app/api/v1/auth/create-key" \
        -H "Content-Type: application/json" \
        -d '{"name": "your-app-name"}'
   ```

## ⚡ Quick Start

1. Make sure your MCP server is running with the updated `server.py`
2. Ensure your `.env` file contains the required API configuration
3. Ask natural language questions about repair costs
4. Use specific repair type names for detailed estimates
5. Include zip codes for accurate regional pricing

**Happy repair cost planning! 🏠💰**