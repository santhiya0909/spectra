"use client";

import React, { useState, useEffect, useRef, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { useQuery, useMutation } from "@tanstack/react-query";
import { aiService, AIChatResponse } from "@/services/ai.service";
import { subjectService, Subject } from "@/services/subject.service";
import { RoleLayout } from "@/components/layout/RoleLayout";
import { Badge } from "@/components/common/Badge";
import {
  Bot,
  Send,
  User,
  Loader2,
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
    "Explain pass-by-value with Java functions",
    "Why does recursion cause a StackOverflowError?",
    "Give me a targeted code puzzle on function parameters",
    "How does method overloading work in Java?",
  ];

  return (
    <div className="flex h-[calc(100vh-7rem)] flex-col gap-4">
      {/* Tutor Header & Context Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 rounded-2xl border border-slate-200 bg-white px-5 py-3.5 shadow-sm">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-gradient-to-tr from-brand-600 via-secondary-500 to-accent-500 text-white shadow-md shadow-brand-500/20">
            <Bot className="h-5 w-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="font-bold text-slate-900 text-sm sm:text-base">SPECTRA Socratic Tutor</h2>
              <Badge variant="cyan" size="sm">
                Active Recall Engine
              </Badge>
            </div>
            <p className="text-xs text-slate-500">Context-aware tutor grounded in your performance diagnostic</p>
          </div>
        </div>

        {/* Context Selector */}
        <div className="flex items-center gap-2">
          <select
            value={selectedSubjectId || ""}
            onChange={(e) => setSelectedSubjectId(Number(e.target.value))}
            className="rounded-xl border border-slate-200 bg-slate-50 px-3 py-1.5 text-xs font-semibold text-slate-700 outline-none focus:border-brand-500"
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
      <div className="flex-1 overflow-y-auto rounded-3xl border border-slate-200 bg-white p-4 sm:p-6 shadow-sm space-y-4">
        {messages.map((m, idx) => (
          <div
            key={idx}
            className={`flex gap-3 max-w-3xl ${m.role === "user" ? "ml-auto flex-row-reverse" : "mr-auto"}`}
          >
            <div className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-xl text-xs font-bold ${
              m.role === "user" ? "bg-slate-900 text-white" : "bg-brand-50 text-brand-700 border border-brand-200"
            }`}>
              {m.role === "user" ? <User className="h-4 w-4" /> : <Bot className="h-4 w-4" />}
            </div>

            <div
              className={`rounded-2xl p-4 text-xs sm:text-sm leading-relaxed ${
                m.role === "user"
                  ? "bg-brand-600 text-white shadow-sm"
                  : "bg-slate-50 border border-slate-200/80 text-slate-800"
              }`}
            >
              <div className="whitespace-pre-wrap">{m.content}</div>
            </div>
          </div>
        ))}

        {chatMutation.isPending && (
          <div className="flex gap-3 mr-auto max-w-xl">
            <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-xl bg-brand-50 text-brand-700 border border-brand-200 text-xs">
              <Bot className="h-4 w-4" />
            </div>
            <div className="rounded-2xl bg-slate-50 border border-slate-200 p-3.5 text-xs text-slate-500 flex items-center gap-2">
              <Loader2 className="h-4 w-4 animate-spin text-brand-600" />
              <span>Formulating personalized pedagogical response...</span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Quick Prompts */}
      <div className="flex flex-wrap gap-2">
        {samplePrompts.map((p, i) => (
          <button
            key={i}
            onClick={() => handleSend(p)}
            disabled={chatMutation.isPending}
            className="rounded-xl border border-slate-200 bg-white px-3 py-1.5 text-xs text-slate-600 hover:border-brand-300 hover:bg-brand-50 hover:text-brand-700 transition"
          >
            &ldquo;{p}&rdquo;
          </button>
        ))}
      </div>

      {/* Input Bar */}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          handleSend();
        }}
        className="flex items-center gap-2 rounded-2xl border border-slate-200 bg-white p-2 shadow-sm"
      >
        <input
          type="text"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          placeholder="Ask a question about Java functions, parameters, or diagnostic mistakes..."
          className="flex-1 bg-transparent px-3 py-2 text-sm text-slate-900 outline-none placeholder:text-slate-400"
        />
        <button
          type="submit"
          disabled={!inputMessage.trim() || chatMutation.isPending}
          className="flex h-10 w-10 items-center justify-center rounded-xl bg-brand-600 text-white shadow hover:bg-brand-700 transition disabled:opacity-40"
        >
          <Send className="h-4 w-4" />
        </button>
      </form>
    </div>
  );
}

export default function StudentAITutorPage() {
  return (
    <RoleLayout allowedRoles={["STUDENT", "ADMIN"]}>
      <Suspense fallback={<div className="p-8 text-center text-slate-400">Loading AI Socratic Tutor...</div>}>
        <AITutorChatContent />
      </Suspense>
    </RoleLayout>
  );
}
