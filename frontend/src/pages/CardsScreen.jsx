import React from "react";
import { useNavigate } from "react-router-dom";
import { CreditCard, Lock } from "lucide-react";
import BottomNav from "@/components/BottomNav";

const cards = [
  { id: 1, type: "Current Account", number: "****4821", balance: "£3,842.50", active: true },
  { id: 2, type: "Savings", number: "****7192", balance: "£12,430.00", active: true },
];

const CardsScreen = () => {
  const navigate = useNavigate();
  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto px-6 pb-4">
        <div className="pt-6 pb-2 fade-in">
          <p className="text-body text-muted-foreground">Your</p>
          <h1 className="text-balance text-foreground">Cards.</h1>
          <p className="text-body text-muted-foreground mt-2">
            Manage your accounts and cards.
          </p>
        </div>

        <div className="space-y-4 mt-4 slide-up">
          {cards.map((card) => (
            <button
              key={card.id}
              onClick={() => navigate(`/card/${card.id}/transactions`)}
              className="btn-press w-full text-left rounded-2xl p-6 bg-secondary text-secondary-foreground"
            >
              <div className="flex items-center justify-between mb-6">
                <CreditCard size={28} />
                <span className="text-xs font-semibold opacity-70 uppercase tracking-wider">
                  {card.active ? "Active" : "Frozen"}
                </span>
              </div>
              <p className="text-2xl font-mono font-semibold tracking-widest mb-4">{card.number}</p>
              <div className="flex justify-between items-end">
                <div>
                  <p className="text-xs opacity-70">{card.type}</p>
                  <p className="text-xl font-semibold">{card.balance}</p>
                </div>
                <Lock size={18} className="opacity-50" />
              </div>
            </button>
          ))}
        </div>
      </div>
      <BottomNav />
    </div>
  );
};

export default CardsScreen;
