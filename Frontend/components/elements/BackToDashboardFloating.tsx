"use client";

import { usePathname, useRouter } from "next/navigation";
import { ChevronLeft } from "lucide-react";

import { Button } from "@/components/ui/button";

export default function BackToDashboardFloating() {
  const router = useRouter();
  const pathname = usePathname();

  if (!pathname || pathname === "/dashboard") return null;

  return (
    <div className="fixed top-4 right-4 z-50">
      {/* <Button variant="outline" size="sm" onClick={() => router.push("/dashboard")}>
        <ChevronLeft className="h-4 w-4 mr-1" />
        Back to Dashboard
      </Button> */}
    </div>
  );
}
