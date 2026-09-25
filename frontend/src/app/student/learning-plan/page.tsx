"use client";

import React from "react";
import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { studentService } from "@/services/student.service";
import { RoleLayout } from "@/components/layout/RoleLayout";
import { Badge } from "@/components/common/Badge";
import {
  Compass,
  CheckCircle2,
  PlayCircle,
  BookOpen,
  HelpCircle,
  AlertCircle,
  RefreshCw
} from "lucide-react";

export default function StudentLearningPlanPage() {
  const { data: plan, isLoading, error, refetch, isFetching } = useQuery({
    queryKey: ["learningPlan"],
    queryFn: studentService.getLearningPlan,
  });

  const planItems = Array.isArray(plan?.items) ? plan.items : [];

  return (
    <RoleLayout allowedRoles={["STUDENT", "ADMIN"]}>
      <div className="mx-auto max-w-4xl space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="flex h-2 w-2 rounded-full bg-brand-500 animate-pulse" />
              <span className="text-xs font-bold uppercase tracking-wider text-brand-600">Dynamic Roadmap</span>
            </div>
            <h1 className="text-2xl font-bold tracking-tight text-slate-900">Personalized Learning Roadmap</h1>
            <p className="mt-1 text-sm text-slate-500">
              A sequenced action plan automatically ordered by priority to maximize knowledge acquisition.
            </p>
          </div>

          <button
            onClick={() => refetch()}
            disabled={isFetching}
            className="inline-flex items-center gap-1.5 rounded-xl border border-slate-200 bg-white px-3.5 py-2 text-xs font-semibold text-slate-700 shadow-sm hover:bg-slate-50 disabled:opacity-50 self-start sm:self-center"
          >
            <RefreshCw className={`h-3.5 w-3.5 text-slate-500 ${isFetching ? "animate-spin" : ""}`} />
            <span>Refresh</span>
          </button>
        </div>

        {isLoading ? (
          <div className="space-y-4 animate-pulse">
            {[1, 2, 3].map((i) => (
              <div key={i} className="h-28 bg-slate-200 rounded-2xl" />
            ))}
          </div>
        ) : error ? (
          <div className="rounded-2xl border border-rose-200 bg-rose-50 p-6 text-center text-rose-700">
            <AlertCircle className="h-8 w-8 mx-auto mb-2 text-rose-600" />
            <h3 className="font-bold text-sm">Failed to load learning plan</h3>
            <p className="text-xs text-rose-600 mt-1">{(error as any)?.message || "Please try again."}</p>
            <button
              onClick={() => refetch()}
              className="mt-4 inline-flex items-center gap-1.5 rounded-xl bg-rose-600 px-4 py-2 text-xs font-semibold text-white shadow hover:bg-rose-700"
            >
              <RefreshCw className="h-3.5 w-3.5" />
              <span>Retry</span>
            </button>
          </div>
        ) : planItems.length > 0 ? (
          <div className="relative pl-6 space-y-6 before:absolute before:left-2.5 before:top-3 before:bottom-3 before:w-0.5 before:bg-slate-200">
            {planItems.map((item: any, idx: number) => {
              const isLesson = item.resource_type === "LESSON";

              return (
                <div key={item.id} className="relative">
                  {/* Step Marker */}
                  <div className={`absolute -left-6 top-1.5 flex h-5 w-5 items-center justify-center rounded-full text-[10px] font-bold ${
                    item.completed
                      ? "bg-emerald-600 text-white"
                      : "border-2 border-brand-600 bg-white text-brand-600 shadow"
                  }`}>
                    {idx + 1}
                  </div>

                  {/* Card Content */}
                  <div className="rounded-3xl border border-slate-200 bg-white p-5 sm:p-6 shadow-sm hover:border-brand-200 transition">
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                      <div className="flex items-start gap-3.5">
                        <div className={`mt-0.5 flex h-9 w-9 shrink-0 items-center justify-center rounded-xl ${
                          isLesson ? "bg-brand-50 text-brand-600" : "bg-purple-50 text-purple-600"
                        }`}>
                          {isLesson ? <BookOpen className="h-5 w-5" /> : <HelpCircle className="h-5 w-5" />}
                        </div>
                        <div>
                          <div className="flex items-center gap-2">
                            <Badge variant={isLesson ? "brand" : "purple"} size="sm">
                              {item.resource_type}
                            </Badge>
                            {item.completed && (
                              <span className="flex items-center gap-1 text-[11px] font-bold text-emerald-600">
                                <CheckCircle2 className="h-3.5 w-3.5" /> Completed
                              </span>
                            )}
                          </div>
                          <h3 className="text-base font-bold text-slate-900 mt-1">{item.title}</h3>
                          <p className="text-xs text-slate-500 mt-0.5">{item.description}</p>
                        </div>
                      </div>

                      <Link
                        href={isLesson ? `/student/lessons/${item.resource_id}` : `/student/quizzes/${item.resource_id}`}
                        className="inline-flex items-center gap-1.5 rounded-xl bg-slate-900 px-4 py-2 text-xs font-bold text-white hover:bg-brand-600 transition shadow self-start sm:self-center"
                      >
                        <PlayCircle className="h-4 w-4" />
                        <span>Start Activity</span>
                      </Link>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        ) : (
          <div className="rounded-3xl border border-dashed border-slate-300 bg-white p-12 text-center text-slate-500">
            <Compass className="h-10 w-10 mx-auto text-slate-400 mb-2" />
            <h3 className="font-bold text-slate-900">No active learning plan</h3>
            <p className="text-xs text-slate-500 mt-1">Complete a quiz assessment to generate your personalized learning roadmap!</p>
            <Link
              href="/student/quizzes"
              className="mt-4 inline-block rounded-xl bg-brand-600 px-4 py-2 text-xs font-semibold text-white shadow"
            >
              Take Quiz
            </Link>
          </div>
        )}
      </div>
    </RoleLayout>
  );
}
