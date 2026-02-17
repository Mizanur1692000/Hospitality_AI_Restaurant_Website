"use client";

import { useState, useRef, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import {
  BarChart3,
  Users,
  Wine,
  ChefHat,
  Lightbulb,
  TrendingUp,
  FileSpreadsheet,
  Send,
  Paperclip,
  User,
  BotIcon,
  Plus,
} from "lucide-react";
import { cn } from "@/lib/utils";

const mainCards = [
  {
    id: "kpi",
    title: "KPI Analysis",
    icon: BarChart3,
    iconBg: "bg-purple-600",
    route: "/dashboard/kpi-analysis",
  },
  {
    id: "hr",
    title: "HR Optimizations",
    icon: Users,
    iconBg: "bg-green-600",
    route: "/dashboard/hr-optimization",
  },
  {
    id: "beverage",
    title: "Beverage Insights",
    icon: Wine,
    iconBg: "bg-red-600",
    route: "/dashboard/beverage-insights",
  },
  {
    id: "menu",
    title: "Menu Engineering",
    icon: ChefHat,
    iconBg: "bg-pink-600",
    route: "/dashboard/menu-engineering",
  },
  {
    id: "recipe",
    title: "Recipe Intelligence",
    icon: Lightbulb,
    iconBg: "bg-blue-600",
    route: "/dashboard/recipe-intelligence",
  },
  {
    id: "strategic",
    title: "Strategic Planning",
    icon: TrendingUp,
    iconBg: "bg-cyan-600",
    route: "/dashboard/strategic-planning",
  },
];

const quickActions = [
  {
    id: "sales-forecasting",
    label: "Sales forecasting",
    prompt:
      "I'd be happy to help with sales forecasting! To provide accurate predictions, please share:\n\n• Historical sales data (last 6-12 months)\n• Current revenue figures\n• Seasonal patterns or trends\n• Any upcoming events or promotions\n• Your target time period for forecasting\n\nYou can upload a CSV file or paste the data directly.",
  },
  {
    id: "menu-profitability",
    label: "Menu profitability",
    prompt:
      "Great! Let's analyze your menu profitability. I'll need:\n\n• Menu item names and prices\n• Cost of ingredients for each dish\n• Sales volume per item\n• Food cost percentage targets\n• Labor costs associated with preparation\n\nPlease share this information or upload your menu data file.",
  },
  {
    id: "prime-cost",
    label: "Prime cost analysis",
    prompt:
      "I'll help you analyze your prime costs. Please provide:\n\n• Total food costs\n• Total beverage costs\n• Total labor costs (including wages, taxes, benefits)\n• Total sales/revenue\n• Time period for analysis\n\nThis will help me calculate your prime cost percentage and identify optimization opportunities.",
  },
  {
    id: "waste-pattern",
    label: "Waste pattern detection",
    prompt:
      "Let's identify waste patterns in your operation. I need:\n\n• Daily/weekly waste logs\n• Categories of waste (spoilage, prep waste, plate waste)\n• Inventory levels\n• Purchase records\n• Any existing tracking data\n\nShare your waste tracking data to get detailed insights and recommendations.",
  },
  {
    id: "ingredient-cost",
    label: "Ingredient cost breakdown",
    prompt:
      "I'll break down your ingredient costs. Please provide:\n\n• List of all ingredients used\n• Purchase prices per unit\n• Quantities used per recipe\n• Supplier information\n• Frequency of purchases\n\nYou can upload invoices or inventory spreadsheets for detailed analysis.",
  },
  {
    id: "pricing-recommendations",
    label: "Pricing recommendations",
    prompt:
      "Let me help optimize your pricing strategy. I need:\n\n• Current menu prices\n• Food and labor costs per item\n• Target profit margins\n• Competitor pricing (if available)\n• Sales data by menu item\n• Your market positioning strategy\n\nShare this information for data-driven pricing recommendations.",
  },
];

interface Message {
  id: number;
  type: "user" | "ai";
  text: string;
}

export default function NewChat() {
  const router = useRouter();
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const scrollContainerRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleCardClick = (route: string) => {
    router.push(route);
  };

  const handleQuickAction = (prompt: string) => {
    const aiMessage: Message = {
      id: messages.length + 1,
      type: "ai",
      text: prompt,
    };
    setMessages([...messages, aiMessage]);
  };

  const handleSendMessage = () => {
    if (inputValue.trim()) {
      const userMessage: Message = {
        id: messages.length + 1,
        type: "user",
        text: inputValue,
      };
      setMessages([...messages, userMessage]);
      setInputValue("");

      // Simulate AI response
      setTimeout(() => {
        const aiResponse: Message = {
          id: messages.length + 2,
          type: "ai",
          text: "Thank you for providing that information. I'm analyzing your data now. Please give me a moment to generate insights and recommendations based on what you've shared.",
        };
        setMessages((prev) => [...prev, aiResponse]);
      }, 1000);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="h-full flex flex-col bg-white dark:bg-black">
      {/* Chat Messages Area - Scrollable */}
      <div
        ref={scrollContainerRef}
        className="flex-1 overflow-y-auto px-4 py-8"
      >
        <div className="max-w-6xl mx-auto">
          {/* Header */}
          <div className="text-center mb-8 sm:mb-12">
            <h1 className="bg-gradient-to-r from-[#C27AFF] via-[#51A2FF] to-[#C27AFF] bg-clip-text text-transparent text-3xl sm:text-4xl lg:text-5xl font-semibold mb-3 sm:mb-4">
              Your Hospitality AI Assistant
            </h1>
            <p className="text-gray-500 dark:text-gray-400 text-sm sm:text-base lg:text-lg px-4">
              Ask anything about restaurant KPIs, staffing, purchasing, menu
              <br className="hidden sm:block" />
              engineering, beverage management, or financial strategy.
            </p>
          </div>

          {/* Main Feature Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6 mb-8">
            {mainCards.map((card) => {
              const Icon = card.icon;
              return (
                <Card
                  key={card.id}
                  onClick={() => handleCardClick(card.route)}
                  className="p-6 cursor-pointer transition-all duration-300 hover:scale-105 
           bg-gradient-to-br from-gray-200 to-gray-100 
           dark:from-gray-900 dark:to-gray-700 
           border border-gray-300 dark:border-gray-800 
           hover:border-gray-400 dark:hover:border-gray-600"
                >
                  <div className="space-y-4">
                    <div
                      className={cn(
                        "w-12 h-12 rounded-xl flex items-center justify-center",
                        card.iconBg
                      )}
                    >
                      <Icon className="w-6 h-6 text-white" />
                    </div>
                    <h3 className="text-lg font-semibold text-black dark:text-white">
                      {card.title}
                    </h3>
                  </div>
                </Card>
              );
            })}
          </div>

          {/* Quick Actions */}
          <div className="flex flex-wrap gap-3 justify-center mb-8">
            {quickActions.map((action) => (
              <Button
                key={action.id}
                onClick={() => handleQuickAction(action.prompt)}
                variant="secondary"
                className="bg-gray-200 dark:bg-gray-700 hover:bg-gray-600 dark:hover:bg-gray-600 text-black dark:text-white border-0 rounded-full px-4 py-2 text-sm"
              >
                <Plus className="w-4 h-4 mr-1.5" />
                {action.label}
              </Button>
            ))}
          </div>

          {/* Chat Messages */}
          {messages.length > 0 ? (
            <div className="space-y-4 pb-4">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={cn(
                    "flex gap-3",
                    message.type === "user" ? "justify-end" : "justify-start"
                  )}
                >
                  {message.type === "ai" && (
                    <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-purple-600 to-blue-600 flex items-center justify-center flex-shrink-0">
                      <BotIcon className="w-5 h-5 text-white" />
                    </div>
                  )}

                  <div
                    className={cn(
                      "max-w-3xl rounded-2xl px-6 py-4",
                      message.type === "user"
                        ? "bg-gradient-to-br from-[#9810FA] to-[#155DFC] text-white"
                        : "bg-gray-100 dark:bg-[#1E2939] text-gray-900 dark:text-white"
                    )}
                  >
                    <p className="whitespace-pre-wrap">{message.text}</p>
                  </div>

                  {message.type === "user" && (
                    <div className="w-10 h-10 rounded-lg bg-gray-600 dark:bg-gray-700 flex items-center justify-center flex-shrink-0">
                      <User className="w-5 h-5 text-white" />
                    </div>
                  )}
                </div>
              ))}
              {/* Invisible div to scroll to */}
              <div ref={messagesEndRef} />
            </div>
          ):(
            <div className="min-h-[135px]"/>
          )}
        </div>
      </div>

      {/* Input Area - Fixed at Bottom */}
      <div className="sticky bottom-0 border-t border-gray-200 dark:border-gray-800 bg-white dark:bg-black">
        <div className="max-w-6xl mx-auto p-4">
          <div className="flex gap-2 items-center bg-gray-100 dark:bg-[#1E2939] rounded-xl px-4 py-3 border border-gray-300 dark:border-gray-700">
            <Button
              variant="ghost"
              size="icon"
              className="text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300"
            >
              <Paperclip className="w-5 h-5" />
            </Button>
            <Textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={handleKeyPress}
              placeholder="Ask me anything about your restaurant KPIs, staffing, food cost, beverage cost, or business strategy..."
              className="flex-1 resize-none overflow-hidden min-h-[20px] max-h-32 bg-transparent border-none text-gray-900 dark:text-white placeholder:text-gray-500 dark:placeholder:text-gray-500 focus-visible:ring-0 focus-visible:ring-offset-0"
              rows={1}
            />
            <Button
              onClick={handleSendMessage}
              size="icon"
              className="bg-blue-600 hover:bg-blue-700 text-white rounded-lg flex-shrink-0"
            >
              <Send className="w-4 h-4" />
            </Button>
          </div>
          <p className="text-center text-xs text-gray-500 dark:text-gray-500 mt-2">
            Press Enter to send, Shift + Enter for new line
          </p>
        </div>
      </div>
    </div>
  );
}
