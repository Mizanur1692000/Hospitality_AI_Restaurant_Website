"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { CheckCircle2 } from "lucide-react"
import { Button } from "@/components/ui/button"

export default function VerificationSuccessPage() {
  const router = useRouter()
  const [countdown, setCountdown] = useState(5)

  useEffect(() => {
    const timer = setInterval(() => {
      setCountdown((prev) => prev - 1)
    }, 1000)

    return () => clearInterval(timer)
  }, [])

  useEffect(() => {
    if (countdown === 0) {
      router.push("/dashboard")
    }
  }, [countdown, router])

  const handleContinue = () => {
    router.push("/dashboard")
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-white dark:bg-black p-4">
      <div className="w-full max-w-md">
        {/* Success Container */}
        <div className="bg-white dark:bg-gray-900/50 border border-gray-200 dark:border-gray-800 rounded-2xl p-12 text-center space-y-6">
          {/* Success Icon with Animation */}
          <div className="flex justify-center">
            <div className="relative">
              {/* Outer rings */}
              <div className="absolute inset-0 rounded-full bg-green-500/20 animate-ping" />
              <div className="absolute inset-2 rounded-full bg-green-500/20 animate-ping animation-delay-150" />
              
              {/* Main icon */}
              <div className="relative w-24 h-24 rounded-full bg-gradient-to-br from-green-400 to-green-600 flex items-center justify-center">
                <CheckCircle2 className="w-12 h-12 text-white" strokeWidth={2.5} />
              </div>
            </div>
          </div>

          {/* Success Message */}
          <div className="space-y-3">
            <h2 className="text-2xl font-semibold text-gray-900 dark:text-white">
              Verification Successful!
            </h2>
            <p className="text-gray-600 dark:text-gray-400 text-sm max-w-sm mx-auto">
              Congratulations! Your email has been successfully verified. Your account is now active
              and ready to use.
            </p>
          </div>

          {/* Continue Button */}
          <div className="space-y-3 pt-4">
            <Button
              onClick={handleContinue}
              className="w-full bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white font-medium py-6 rounded-xl"
            >
              Continue to Dashboard
            </Button>
            
            {/* Auto redirect message */}
            {countdown > 0 && (
              <p className="text-xs text-gray-500 dark:text-gray-400">
                Automatically redirecting in {countdown} seconds...
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}