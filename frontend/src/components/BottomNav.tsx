import React from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { Home, CreditCard, HelpCircle } from "lucide-react";

const tabs = [
  { label: "Home", icon: Home, path: "/dashboard" },
  { label: "Cards", icon: CreditCard, path: "/cards" },
  { label: "Support", icon: HelpCircle, path: "/support" },
];

const BottomNav: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <nav
      className="flex items-center justify-around bg-card border-t border-border px-2 py-2"
      role="tablist"
      aria-label="Main navigation"
    >
      {tabs.map((tab) => {
        const isActive =
          location.pathname === tab.path ||
          (tab.path === "/dashboard" && location.pathname.startsWith("/send"));
        const Icon = tab.icon;

        return (
          <button
            key={tab.label}
            role="tab"
            aria-selected={isActive}
            aria-label={tab.label}
            onClick={() => navigate(tab.path)}
            className={`btn-press flex flex-col items-center gap-1 min-w-[72px] min-h-[48px] px-3 py-1.5 rounded-xl transition-colors ${
              isActive
                ? "bg-primary/10 text-primary"
                : "text-muted-foreground hover:text-foreground"
            }`}
          >
            <Icon size={24} strokeWidth={isActive ? 2.5 : 2} />
            <span className={`text-xs font-semibold ${isActive ? "text-primary" : ""}`}>
              {tab.label}
            </span>
          </button>
        );
      })}
    </nav>
  );
};

export default BottomNav;
