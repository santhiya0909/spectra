"use client";

import React from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { adminService } from "@/services/admin.service";
import { RoleLayout } from "@/components/layout/RoleLayout";
import { Badge } from "@/components/common/Badge";
import { Users, Shield, Loader2 } from "lucide-react";

export default function AdminUsersPage() {
  const queryClient = useQueryClient();

  const { data: users, isLoading } = useQuery({
    queryKey: ["adminUsers"],
    queryFn: adminService.getUsers,
  });

  const roleMutation = useMutation({
    mutationFn: ({ id, role }: { id: number; role: string }) =>
      adminService.updateUserRole(id, role),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["adminUsers"] });
      queryClient.invalidateQueries({ queryKey: ["adminDashboard"] });
    },
  });

  return (
    <RoleLayout allowedRoles={["ADMIN"]}>
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-white">User &amp; Role Management</h1>
          <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
            Audit registered system accounts, assign RBAC privileges, and regulate role access.
          </p>
        </div>

        <div className="rounded-3xl border border-slate-200 dark:border-white/[0.08] bg-white dark:bg-[#0B1124]/85 p-6 shadow-sm">
          {isLoading ? (
            <div className="space-y-3 animate-pulse">
              {[1, 2, 3].map((i) => (
                <div key={i} className="h-14 bg-slate-100 dark:bg-white/[0.04] rounded-xl" />
              ))}
            </div>
          ) : users && users.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="border-b border-slate-200 dark:border-white/[0.06] bg-slate-50 dark:bg-white/[0.03] text-[11px] font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500">
                  <tr>
                    <th className="px-4 py-3">User Name</th>
                    <th className="px-4 py-3">Email Address</th>
                    <th className="px-4 py-3">Current Role</th>
                    <th className="px-4 py-3">Account Created</th>
                    <th className="px-4 py-3 text-right">Change Role</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 dark:divide-white/[0.04]">
                  {users.map((u: any) => (
                    <tr key={u.id} className="hover:bg-slate-50 dark:hover:bg-white/[0.03] transition">
                      <td className="px-4 py-3.5 font-bold text-slate-900 dark:text-white">{u.name}</td>
                      <td className="px-4 py-3.5 text-slate-600 dark:text-slate-300">{u.email}</td>
                      <td className="px-4 py-3.5">
                        <Badge
                          variant={u.role === "STUDENT" ? "cyan" : u.role === "TEACHER" ? "purple" : "emerald"}
                          size="sm"
                        >
                          {u.role}
                        </Badge>
                      </td>
                      <td className="px-4 py-3.5 text-slate-400">
                        {new Date(u.created_at).toLocaleDateString()}
                      </td>
                      <td className="px-4 py-3.5 text-right">
                        <select
                          value={u.role}
                          onChange={(e) => roleMutation.mutate({ id: u.id, role: e.target.value })}
                          disabled={roleMutation.isPending}
                          className="rounded-lg border border-slate-200 dark:border-white/[0.08] bg-white dark:bg-white/[0.06] px-2.5 py-1 text-xs font-semibold text-slate-700 dark:text-slate-300 outline-none focus:border-brand-500 dark:focus:border-cyan-500"
                        >
                          <option value="STUDENT">STUDENT</option>
                          <option value="TEACHER">TEACHER</option>
                          <option value="ADMIN">ADMIN</option>
                        </select>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p className="text-xs text-slate-400 py-6 text-center">No users found.</p>
          )}
        </div>
      </div>
    </RoleLayout>
  );
}
