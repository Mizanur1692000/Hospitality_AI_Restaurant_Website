# Hospitality AI — Frontend

Next.js dashboard for the Hospitality AI Platform. Provides a modern, responsive UI for restaurant operators to interact with AI-driven analytics covering KPIs, Menu Engineering, Beverage Management, HR Optimization, Recipe Intelligence, and Strategic Planning.

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | Next.js 16 (App Router) |
| Language | TypeScript / React 19 |
| Styling | Tailwind CSS + shadcn/ui (Radix UI) |
| Charts | Recharts |
| Animation | Motion (Framer Motion) |
| Forms | React Hook Form + Zod |
| Theming | next-themes (dark / light mode) |
| Sanitization | DOMPurify |

## Project Structure

```
Frontend/
├── app/
│   ├── auth/                    # Login & authentication pages
│   ├── dashboard/
│   │   ├── beverage-insights/   # Liquor cost, bar inventory, beverage pricing
│   │   ├── csv-kpi-dashboard/   # CSV-based KPI upload & reporting
│   │   ├── history/             # Analysis history log
│   │   ├── hr-optimization/     # Labor & HR analytics
│   │   ├── kpi-analysis/        # Prime cost, food cost, sales performance
│   │   ├── menu-engineering/    # Product mix, pricing strategy, item optimization
│   │   ├── profile/             # User profile settings
│   │   ├── recipe-intelligence/ # Recipe cost & optimization
│   │   └── strategic-planning/  # Strategic business insights
│   ├── layout.tsx               # Root layout with theme provider
│   └── page.tsx                 # Landing / redirect page
├── components/
│   ├── auth/                    # Auth-specific components
│   ├── dashboard/               # Dashboard feature components
│   ├── elements/                # Shared UI elements
│   └── ui/                      # shadcn/ui base components
├── services/                    # API service layer (one file per domain)
│   ├── beverageService.ts
│   ├── hrService.ts
│   ├── kpiService.ts
│   ├── menuService.ts
│   ├── recipeService.ts
│   └── strategicService.ts
├── hooks/                       # Custom React hooks
├── lib/                         # Utility functions
└── providers/                   # React context providers
```

## Getting Started

### Prerequisites

- Node.js 18+
- Backend running at `http://localhost:8000` (see `../Backend/README.md`)

### Install & Run

```bash
cd Frontend
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Available Scripts

| Script | Description |
|---|---|
| `npm run dev` | Start development server |
| `npm run build` | Build for production |
| `npm start` | Start production server |
| `npm run lint` | Run ESLint |

## Environment Variables

Create a `.env.local` file in the `Frontend/` directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Update the value to match your backend URL in staging or production.

## Dashboard Modules

| Module | Route | Description |
|---|---|---|
| KPI Analysis | `/dashboard/kpi-analysis` | Prime cost, labor, food cost & sales analytics |
| CSV KPI Dashboard | `/dashboard/csv-kpi-dashboard` | Upload CSV files for batch KPI reporting |
| Beverage Insights | `/dashboard/beverage-insights` | Liquor cost, bar inventory & beverage pricing |
| Menu Engineering | `/dashboard/menu-engineering` | Product mix, menu pricing & item optimization |
| HR Optimization | `/dashboard/hr-optimization` | Labor scheduling & HR cost analysis |
| Recipe Intelligence | `/dashboard/recipe-intelligence` | Recipe costing & ingredient optimization |
| Strategic Planning | `/dashboard/strategic-planning` | High-level business strategy insights |
| History | `/dashboard/history` | Log of past analyses |
| Profile | `/dashboard/profile` | User account settings |

## API Integration

All dashboard modules communicate with the Django backend via the service layer in `services/`. The unified backend endpoint is:

```
POST /api/agent/        # JSON & CSV task endpoint
POST /api/agent/safe/   # Business insight card endpoint
```

Refer to `../Backend/README.md` for the full API reference and task catalog.

## Deployment

### Vercel (recommended)

```bash
npm run build
# Deploy via Vercel CLI or connect the GitHub repo to vercel.com
```

### Docker / Self-hosted

```bash
npm run build
npm start
```

Set `NEXT_PUBLIC_API_URL` to point to your production backend before building.
