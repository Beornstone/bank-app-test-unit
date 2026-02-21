import React from "react";
import { useNavigate } from "react-router-dom";
import { Send, ClockArrowUp, HelpCircle, ArrowDownLeft, ArrowUpRight } from "lucide-react";
import BottomNav from "@/components/BottomNav";

const transactions = [
  { id: 1, name: "Grocery Store", date: "Today", amount: -42.5, type: "out" },
  { id: 2, name: "Sarah (Granddaughter)", date: "Yesterday", amount: -25.0, type: "out" },
  { id: 3, name: "Pension Deposit", date: "Feb 18", amount: 1850.0, type: "in" },
];

const Dashboard: React.FC = () => {
  const navigate = useNavigate();

  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return "Good Morning";
    if (hour < 18) return "Good Afternoon";
    return "Good Evening";
  };

  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto px-5 pb-4">
        {/* Header */}
        <div className="pt-4 pb-6 fade-in">
          <p className="text-body text-muted-foreground">{getGreeting()},</p>
          <h1 className="text-heading-lg text-foreground">Margaret</h1>
        </div>

        {/* Balance Card */}
        <div className="bg-secondary rounded-2xl p-6 mb-6 slide-up">
          <p className="text-sm font-medium text-secondary-foreground/70 mb-1">
            Your Balance
          </p>
          <p className="text-balance text-secondary-foreground">
            £3,842<span className="text-heading">.50</span>
          </p>
          <p className="text-sm text-secondary-foreground/60 mt-2">
            Current Account · ****4821
          </p>
        </div>

        {/* Action Buttons */}
        <div className="grid grid-cols-3 gap-3 mb-6">
          {[
            { label: "Send Money", icon: Send, action: () => navigate("/send") },
            { label: "View History", icon: ClockArrowUp, action: () => {} },
            { label: "Help", icon: HelpCircle, action: () => navigate("/support") },
          ].map((item) => {
            const Icon = item.icon;
            return (
              <button
                key={item.label}
                onClick={item.action}
                className="btn-press flex flex-col items-center gap-2 bg-card rounded-2xl p-4 border border-border hover:border-primary/30 transition-colors min-h-[100px] justify-center slide-up"
                aria-label={item.label}
              >
                <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center">
                  <Icon size={22} className="text-primary" />
                </div>
                <span className="text-sm font-semibold text-foreground leading-tight text-center">
                  {item.label}
                </span>
              </button>
            );
          })}
        </div>

        {/* Recent Activity */}
        <div className="slide-up">
          <h2 className="text-heading-sm text-foreground mb-3">Recent Activity</h2>
          <div className="space-y-2">
            {transactions.map((tx) => (
              <div
                key={tx.id}
                className="flex items-center gap-3 bg-card rounded-xl p-4 border border-border"
              >
                <div
                  className={`w-10 h-10 rounded-full flex items-center justify-center ${
                    tx.type === "in" ? "bg-primary/10" : "bg-muted"
                  }`}
                >
                  {tx.type === "in" ? (
                    <ArrowDownLeft size={18} className="text-primary" />
                  ) : (
                    <ArrowUpRight size={18} className="text-muted-foreground" />
                  )}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-semibold text-foreground truncate">{tx.name}</p>
                  <p className="text-xs text-muted-foreground">{tx.date}</p>
                </div>
                <p
                  className={`text-body font-bold ${
                    tx.type === "in" ? "text-primary" : "text-foreground"
                  }`}
                >
                  {tx.type === "in" ? "+" : "-"}£{Math.abs(tx.amount).toFixed(2)}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>

      <BottomNav />
    </div>
  );
};

export default Dashboard;
