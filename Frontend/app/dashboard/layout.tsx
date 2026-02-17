import MobileHeader from "@/components/elements/MobileHeader"
import Sidebar from "@/components/elements/Sidebar"
import { SidebarInset, SidebarProvider } from "@/components/ui/sidebar"

export default function AppLayout({ children }: { children: React.ReactNode }) {
  return (
    <SidebarProvider>
      <div className="flex h-screen overflow-hidden bg-black dark:bg-black w-full">
        {/* Sidebar */}
        <Sidebar />

        {/* Main Content - Use SidebarInset */}
        <SidebarInset className="flex-1 flex flex-col w-full overflow-hidden">
          {/* Mobile Header */}
          <MobileHeader />

          {/* Main Content Area */}
          <main className="flex-1 overflow-auto w-full">{children}</main>
        </SidebarInset>
      </div>
    </SidebarProvider>
  )
}