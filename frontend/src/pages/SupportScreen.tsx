import React from "react";
import { Phone, MessageCircle, FileText } from "lucide-react";
import BottomNav from "@/components/BottomNav";

const supportOptions = [
  {
    icon: Phone,
    title: "Call Us",
    description: "Speak to a real person. We're here 24/7.",
    action: "0800 123 4567",
  },
  {
    icon: MessageCircle,
    title: "Send a Message",
    description: "We'll reply within 1 hour.",
    action: "Start a chat",
  },
  {
    icon: FileText,
    title: "Common Questions",
    description: "Find answers to common queries.",
    action: "Browse FAQs",
  },
];

const SupportScreen: React.FC = () => {
  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto px-5 pb-4">
        <div className="pt-4 pb-4 fade-in">
          <h1 className="text-heading-lg text-foreground">How Can We Help?</h1>
          <p className="text-body text-muted-foreground mt-1">
            We're always here for you. Choose an option below.
          </p>
        </div>

        <div className="space-y-4">
          {supportOptions.map((option, i) => {
            const Icon = option.icon;
            return (
              <button
                key={i}
                className="btn-press w-full text-left flex items-start gap-4 bg-card rounded-2xl p-5 border border-border hover:border-primary/30 transition-colors slide-up"
                aria-label={option.title}
              >
                <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center shrink-0">
                  <Icon size={22} className="text-primary" />
                </div>
                <div>
                  <p className="text-body font-bold text-foreground">{option.title}</p>
                  <p className="text-sm text-muted-foreground mt-0.5">{option.description}</p>
                  <p className="text-sm font-semibold text-primary mt-2">{option.action}</p>
                </div>
              </button>
            );
          })}
        </div>
      </div>
      <BottomNav />
    </div>
  );
};

export default SupportScreen;
