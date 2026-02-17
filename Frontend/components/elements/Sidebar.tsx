"use client"

import { useState, useEffect } from "react"
import { useRouter, usePathname } from "next/navigation"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import { 
  ChevronLeft, 
  Plus, 
  BarChart3, 
  Users, 
  Wine, 
  ChefHat, 
  Lightbulb, 
  TrendingUp,
  FileSpreadsheet,
  User,
} from "lucide-react"
import { cn } from "@/lib/utils"
import { useSidebar } from "@/components/ui/sidebar"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"

const chatHistory = [
  { id: 1, title: "KPI Analysis - Labor Cost Analysis", href: "/dashboard/kpi-analysis" },
  { id: 2, title: "HR Optimization Review", href: "/dashboard/hr-optimization" },
  { id: 3, title: "Beverage Inventory Check", href: "/dashboard/beverage-insights" },
  { id: 4, title: "Menu Engineering Review", href: "/dashboard/menu-engineering" },
  { id: 5, title: "Recipe Intelligence Analysis", href: "/dashboard/recipe-intelligence" },
  { id: 6, title: "Strategic Planning Session", href: "/dashboard/strategic-planning" },
  { id: 7, title: "CSV KPI Dashboard Review", href: "/dashboard/csv-kpi-dashboard" },
]

const features = [
  { icon: BarChart3, label: "KPI Analysis", href: "/dashboard/kpi-analysis" },
  { icon: Users, label: "HR Optimization", href: "/dashboard/hr-optimization" },
  { icon: Wine, label: "Beverage Insights", href: "/dashboard/beverage-insights" },
  { icon: ChefHat, label: "Menu Engineering", href: "/dashboard/menu-engineering" },
  { icon: Lightbulb, label: "Recipe Intelligence", href: "/dashboard/recipe-intelligence" },
  { icon: TrendingUp, label: "Strategic Planning", href: "/dashboard/strategic-planning" },
  { icon: FileSpreadsheet, label: "CSV KPI Dashboard", href: "/dashboard/csv-kpi-dashboard" },
]

export default function Sidebar() {
  const { open, setOpen } = useSidebar()
  const router = useRouter()
  const pathname = usePathname()
  const [selectedFeature, setSelectedFeature] = useState("KPI Analysis")

  // Update selected feature based on current pathname
  useEffect(() => {
    const currentFeature = features.find(feature => feature.href === pathname)
    if (currentFeature) {
      setSelectedFeature(currentFeature.label)
    }
  }, [pathname])

  const handleFeatureClick = (feature: typeof features[0]) => {
    setSelectedFeature(feature.label)
    router.push(feature.href)
    // Close sidebar on mobile after click
    if (window.innerWidth < 1024) {
      setOpen(false)
    }
  }

  const handleChatHistoryClick = (chat: typeof chatHistory[0]) => {
    router.push(chat.href)
    // Close sidebar on mobile after click
    if (window.innerWidth < 1024) {
      setOpen(false)
    }
  }

  return (
    <>
      {/* Mobile Overlay */}
      {open && (
        <div 
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={() => setOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside
        className={cn(
          "fixed lg:static inset-y-0 left-0 z-50 w-64 flex flex-col bg-gray-100 dark:bg-[#1E2939] border-r border-gray-200 dark:border-gray-800 transition-transform duration-300 ease-in-out",
          open ? "translate-x-0" : "-translate-x-full lg:translate-x-0"
        )}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-800">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-gradient-to-br from-purple-600 to-blue-600 rounded-lg flex items-center justify-center">
              <span className="text-white text-sm font-bold">H</span>
            </div>
            <div>
              <div className="font-semibold text-sm text-gray-900 dark:text-white">Hospitality AI</div>
              <div className="text-xs text-green-500 flex items-center gap-1">
                <span className="w-1.5 h-1.5 bg-green-500 rounded-full animate-pulse"></span>
                AI Assistant Active
              </div>
            </div>
          </div>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setOpen(false)}
            className="lg:hidden"
          >
            <ChevronLeft className="h-5 w-5" />
          </Button>
        </div>

        {/* New Chat Button */}
        <div className="p-4">
          <Button 
            className="w-full bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white font-medium"
            onClick={() => {
              router.push("/dashboard")
              if (window.innerWidth < 1024) setOpen(false)
            }}
          >
            <Plus className="mr-2 h-4 w-4" />
            New Chat
          </Button>
        </div>

        {/* Chat History */}
        <div className="px-4 mb-4">
          <h3 className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-2">
            Chat History
          </h3>
          <ScrollArea className="h-48">
            <div className="space-y-1">
              {chatHistory.map((chat) => (
                <button
                  key={chat.id}
                  onClick={() => handleChatHistoryClick(chat)}
                  className="w-full text-left px-3 py-2 rounded-lg text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-800 transition-colors truncate"
                >
                  {chat.title}
                </button>
              ))}
            </div>
          </ScrollArea>
          <Button variant="outline" className="w-full mt-2" onClick={() => router.push("/dashboard/history")}>
            See all history
          </Button>
        </div>

        {/* Features */}
        <div className="flex-1 px-4 overflow-hidden">
          <h3 className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-2">
            Features
          </h3>
          <ScrollArea className="h-full pb-4">
            <div className="space-y-1">
              {features.map((feature) => {
                const Icon = feature.icon
                const isSelected = selectedFeature === feature.label

                return (
                  <button
                    key={feature.label}
                    onClick={() => handleFeatureClick(feature)}
                    className={cn(
                      "w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-200 group",
                      isSelected
                        ? "bg-gradient-to-r from-purple-600 to-blue-600 text-white shadow-lg"
                        : "text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-800 hover:text-gray-900 dark:hover:text-white"
                    )}
                  >
                    <Icon className={cn("h-4 w-4", isSelected ? "text-white" : "text-gray-500 group-hover:text-current")} />
                    <span>{feature.label}</span>
                    {isSelected && (
                      <div className="ml-auto w-1.5 h-1.5 bg-white rounded-full animate-pulse" />
                    )}
                  </button>
                )
              })}
            </div>
          </ScrollArea>
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-gray-200 dark:border-gray-800 space-y-1">
          <button 
            onClick={() => router.push("/dashboard/profile")}
            className="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-800 transition-colors"
          >
            <User className="h-4 w-4" />
            User Profile
          </button>
          <Select
      defaultValue="en"
      onValueChange={(value) => {
        // handle language change here
        console.log("Selected language:", value)
      }}
    >
      <SelectTrigger className="w-[160px]">
        <SelectValue placeholder="Select language" />
      </SelectTrigger>

      <SelectContent align="end">
        <SelectItem value="en">English</SelectItem>
        <SelectItem value="es">Spanish</SelectItem>
      </SelectContent>
    </Select>
        </div>
      </aside>
    </>
  )
}