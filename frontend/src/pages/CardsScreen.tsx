import React from "react";
import { CreditCard, Lock } from "lucide-react";
import BottomNav from "@/components/BottomNav";

const cards = [
  { type: "Current Account", number: "****4821", balance: "£3,842.50", active: true },
  { type: "Savings", number: "****7192", balance: "£12,430.00", active: true },
];

const CardsScreen: React.FC = () => {
  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto px-5 pb-4">
        <div className="pt-4 pb-4 fade-in">
          <h1 className="text-heading-lg text-foreground">Your Cards</h1>
          <p className="text-body text-muted-foreground mt-1">
            Manage your accounts and cards.
          </p>
        </div>

        <div className="space-y-4">
          {cards.map((card, i) => (
            <div
              key={i}
              className={`rounded-2xl p-6 slide-up ${
                i === 0 ? "bg-secondary text-secondary-foreground" : "bg-primary text-primary-foreground"
              }`}
            >
              <div className="flex items-center justify-between mb-6">
                <CreditCard size={28} />
                <span className="text-xs font-semibold opacity-70 uppercase tracking-wider">
                  {card.active ? "Active" : "Frozen"}
                </span>
              </div>
              <p className="text-2xl font-mono font-bold tracking-widest mb-4">{card.number}</p>
              <div className="flex justify-between items-end">
                <div>
                  <p className="text-xs opacity-70">{card.type}</p>
                  <p className="text-xl font-bold">{card.balance}</p>
                </div>
                <Lock size={18} className="opacity-50" />
              </div>
            </div>
          ))}
        </div>
      </div>
      <BottomNav />
    </div>
  );
};

export default CardsScreen;
