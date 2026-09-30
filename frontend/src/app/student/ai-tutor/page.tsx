"use client";

import React, { useState, useEffect, useRef, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { useQuery, useMutation } from "@tanstack/react-query";
import { aiService, AIChatResponse } from "@/services/ai.service";
import { subjectService, Subject } from "@/services/subject.service";
import { RoleLayout } from "@/components/layout/RoleLayout";
import { GlassCard } from "@/components/common/GlassCard";
import { Badge } from "@/components/common/Badge";
import {
  Bot,
  Send,
  User,
  Loader2,
  Sparkles,
  Zap,
} from "lucide-react";

interface Message {
  role: "user" | "assistant";
  content: string;
}

function AITutorChatContent() {
  const searchParams = useSearchParams();
  const topicParam = searchParams.get("topic");

  const [inputMessage, setInputMessage] = useState("");
  const [selectedSubjectId, setSelectedSubjectId] = useState<number | undefined>(1);
  const [selectedTopicId, setSelectedTopicId] = useState<number | undefined>(
    topicParam ? Number(topicParam) : 2
  );
  const [currentConversationId, setCurrentConversationId] = useState<number | undefined>();
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content:
        "Hello! I am your SPECTRA Intelligent AI Tutor. I analyze your diagnostic quiz results and help you master challenging concepts through Socratic guidance. What would you like to explore today?",
    },
  ]);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const { data: subjects } = useQuery<Subject[]>({
    queryKey: ["subjects"],
    queryFn: subjectService.getSubjects,
  });

  const chatMutation = useMutation({
    mutationFn: (text: string) =>
      aiService.chat({
        message: text,
        conversation_id: currentConversationId,
        subject_id: selectedSubjectId,
        topic_id: selectedTopicId,
        is_during_quiz: false,
      }),
    onSuccess: (data: AIChatResponse) => {
      setCurrentConversationId(data.conversation_id);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: data.reply },
      ]);
    },
  });

  const handleSend = (text?: string) => {
    const toSend = text || inputMessage;
    if (!toSend.trim() || chatMutation.isPending) return;

    setMessages((prev) => [...prev, { role: "user", content: toSend }]);
    if (!text) setInputMessage("");
    chatMutation.mutate(toSend);
  };

  const samplePrompts = [
    "Explain this lesson",
    "Give me a hint",
    "Explain why my answer was incorrect",
    "Give me a similar practice problem",
    "Explain my quiz mistake",
  ];

  return (
    <div className="flex h-[calc(100vh-7rem)] flex-col gap-4">
      {/* Tutor Header & Context Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 rounded-3xl border border-white/[0.08] bg-[#0B1124]/90 px-6 py-4 backdrop-blur-2xl shadow-lg">
        <div className="flex items-center gap-3">
          <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-gradient-to-tr from-cyan-400 via-indigo-600 to-purple-600 text-white shadow-[0_0_20px_rgba(6,182,212,0.4)]">
            <Bot className="h-6 w-6" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="font-bold text-white text-base">SPECTRA Socratic Tutor</h2>
              <span className="text-[10px] font-extrabold uppercase px-2 py-0.5 rounded-full bg-cyan-500/20 text-cyan-300 border border-cyan-500/30">
                Active Recall Engine
              </span>
            </div>
            <p className="text-xs text-slate-400">Context-aware tutor grounded in your performance diagnostic</p>
          </div>
        </div>

        {/* Context Selector */}
        <div className="flex items-center gap-2">
          <select
            value={selectedSubjectId || ""}
            onChange={(e) => setSelectedSubjectId(Number(e.target.value))}
            className="rounded-xl border border-white/10 bg-[#060913] px-3.5 py-2 text-xs font-semibold text-slate-300 outline-none focus:border-cyan-400"
          >
            {subjects?.map((s) => (
              <option key={s.id} value={s.id}>
                {s.name}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Chat Area */}
      <div className="flex-1 overflow-y-auto rounded-3xl border border-white/[0.08] bg-[#070A14]/80 p-4 sm:p-6 backdrop-blur-xl shadow-lg space-y-4">
        {messages.map((m, idx) => (
          <div
            key={idx}
            className={`flex gap-3 max-w-3xl ${m.role === "user" ? "ml-auto flex-row-reverse" : "mr-auto"}`}
          >
            <div
              className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-xl text-xs font-bold ${
                m.role === "user"
                  ? "bg-cyan-500 text-black shadow-[0_0_10px_#22d3ee]"
                  : "bg-purple-950/40 text-purple-300 border border-purple-500/30"
              }`}
            >
              {m.role === "user" ? <User className="h-4 w-4" /> : <Bot className="h-4 w-4" />}
            </div>

            <div
              className={`rounded-2xl p-4 text-xs sm:text-sm leading-relaxed ${
                m.role === "user"
                  ? "bg-gradient-to-r from-cyan-500 to-indigo-600 text-black font-semibold shadow-md shadow-cyan-950/30"
                  : "bg-[#0B1124]/90 border border-white/10 text-slate-200"
              }`}
            >
              <div className="whitespace-pre-wrap">{m.content}</div>
            </div>
          </div>
        ))}

        {chatMutation.isPending && (
          <div className="flex gap-3 max-w-xl mr-auto animate-pulse">
            <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-xl bg-purple-950/40 text-purple-300 border border-purple-500/30">
              <Bot className="h-4 w-4" />
            </div>
            <div className="rounded-2xl bg-[#0B1124]/90 border border-white/10 p-4 text-xs text-slate-400 flex items-center gap-2">
              <Loader2 className="h-4 w-4 animate-spin text-cyan-400" />
              <span>SPECTRA Socratic Tutor is analyzing your concept gap...</span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Suggested Prompts Pill Row */}
      <div className="flex flex-wrap items-center gap-2 px-2">
        {samplePrompts.map((prompt) => (
          <button
            key={prompt}
            type="button"
            onClick={() => handleSend(prompt)}
            className="rounded-xl border border-white/10 bg-white/[0.03] px-3 py-1.5 text-xs font-medium text-slate-300 hover:border-cyan-500/40 hover:bg-white/[0.08] hover:text-white transition"
          >
            {prompt}
          </button>
        ))}
      </div>

      {/* Input Form Bar */}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          handleSend();
        }}
        className="flex items-center gap-2 rounded-2xl border border-white/10 bg-[#0B1124]/90 p-2 backdrop-blur-xl shadow-lg"
      >
        <input
          type="text"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          placeholder="Ask a question about your subject, request a hint, or explain a mistake..."
          disabled={chatMutation.isPending}
          className="flex-1 bg-transparent px-4 py-2 text-xs sm:text-sm text-white placeholder:text-slate-500 focus:outline-none"
        />
        <button
          type="submit"
          disabled={!inputMessage.trim() || chatMutation.isPending}
          className="flex h-10 w-10 items-center justify-center rounded-xl bg-cyan-500 text-black hover:bg-cyan-400 disabled:opacity-40 disabled:cursor-not-allowed shadow-[0_0_12px_rgba(6,182,212,0.3)] transition"
        >
          {chatMutation.isPending ? (
            <Loader2 className="h-4 w-4 animate-spin text-black" />
          ) : (
            <Send className="h-4 w-4" />
          )}
        </button>
      </form>
    </div>
  );
}

export default function AITutorPage() {
  return (
    <RoleLayout allowedRoles={["STUDENT", "ADMIN"]}>
      <Suspense fallback={<div className="p-8 text-center text-slate-400">Loading AI Socratic Environment...</div>}>
        <AITutorChatContent />
      </Suspense>
    </RoleLayout>
  );
}
