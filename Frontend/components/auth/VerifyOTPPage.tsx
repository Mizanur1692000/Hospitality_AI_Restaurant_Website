"use client"

import { useState, useRef } from "react"
import { useRouter } from "next/navigation"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Form, FormControl, FormField, FormItem, FormMessage } from "@/components/ui/form"

const otpSchema = z.object({
  otp: z.string().length(6, "OTP must be 6 digits"),
})

type OTPFormValues = z.infer<typeof otpSchema>

export default function VerifyOTPPage() {
  const [otp, setOtp] = useState<string[]>(["", "", "", "", "", ""])
  const inputRefs = useRef<(HTMLInputElement | null)[]>([])

  const form = useForm<OTPFormValues>({
    resolver: zodResolver(otpSchema),
    defaultValues: {
      otp: "",
    },
  })

  const handleChange = (index: number, value: string) => {
    if (value.length > 1) value = value[0]
    
    const newOtp = [...otp]
    newOtp[index] = value
    setOtp(newOtp)

    // Move to next input
    if (value && index < 5) {
      inputRefs.current[index + 1]?.focus()
    }

    // Update form value
    form.setValue("otp", newOtp.join(""))
  }

  const handleKeyDown = (index: number, e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Backspace" && !otp[index] && index > 0) {
      inputRefs.current[index - 1]?.focus()
    }
  }

  const handlePaste = (e: React.ClipboardEvent) => {
    e.preventDefault()
    const pastedData = e.clipboardData.getData("text").slice(0, 6).split("")
    const newOtp = [...otp]
    
    pastedData.forEach((char, index) => {
      if (index < 6) newOtp[index] = char
    })
    
    setOtp(newOtp)
    form.setValue("otp", newOtp.join(""))
    inputRefs.current[Math.min(pastedData.length, 5)]?.focus()
  }

  const router = useRouter()
  const onSubmit = () => {
    // Navigate to create new password
    router.push("/auth/create-password")
  }

  const handleResendOTP = () => {
    console.log("Resending OTP...")
    // Add resend OTP logic
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-white dark:bg-black p-4">
      <div className="w-full max-w-md">
        {/* Back Button */}
        <Link
          href="/auth/forgot-password"
          className="inline-flex items-center text-sm text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white mb-8 transition-colors"
        >
          ← Back
        </Link>

        {/* Form Container */}
        <div className="bg-white dark:bg-gray-900/50 border border-gray-200 dark:border-gray-800 rounded-2xl p-8 space-y-6">
          {/* Header */}
          <div className="text-center space-y-2">
            <h2 className="text-2xl font-semibold text-gray-900 dark:text-white">Check Your Email</h2>
            <p className="text-gray-600 dark:text-gray-400 text-sm">
              We&apos;ve sent a 6-digit OTP to{" "}
              <span className="font-medium text-gray-900 dark:text-white">you@company.com</span>
              <br />
              Enter the code below to continue.
            </p>
          </div>

          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
              {/* OTP Input */}
              <FormField
                control={form.control}
                name="otp"
                render={() => (
                  <FormItem>
                    <FormControl>
                      <div className="space-y-2">
                        <label className="block text-center text-sm text-gray-700 dark:text-gray-300 mb-4">
                          Enter OTP Code
                        </label>
                        <div className="flex gap-2 justify-center">
                          {otp.map((digit, index) => (
                            <Input
                              key={index}
                              ref={(el) => {
                                inputRefs.current[index] = el
                              }}
                              type="text"
                              inputMode="numeric"
                              maxLength={1}
                              value={digit}
                              onChange={(e) => handleChange(index, e.target.value)}
                              onKeyDown={(e) => handleKeyDown(index, e)}
                              onPaste={handlePaste}
                              className="w-12 h-12 sm:w-14 sm:h-14 text-center text-lg font-semibold bg-gray-50 dark:bg-gray-800/50 border-gray-300 dark:border-gray-700 text-gray-900 dark:text-white focus-visible:ring-purple-500 focus-visible:border-purple-500 rounded-lg"
                            />
                          ))}
                        </div>
                      </div>
                    </FormControl>
                    <FormMessage className="text-red-500 text-center" />
                  </FormItem>
                )}
              />

              {/* Submit Button */}
              <Button
                type="submit"
                className="w-full bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white font-medium py-6 rounded-xl"
              >
                Verify OTP
              </Button>
            </form>
          </Form>

          {/* Resend OTP */}
          <div className="text-center space-y-2">
            <p className="text-sm text-gray-600 dark:text-gray-400">Didn&apos;t receive the code?</p>
            <button
              onClick={handleResendOTP}
              className="text-sm text-purple-600 dark:text-purple-400 hover:text-purple-700 dark:hover:text-purple-300 font-medium transition-colors"
            >
              Resend OTP
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}