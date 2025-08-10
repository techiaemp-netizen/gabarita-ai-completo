'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { Button } from '../components/ui/button';
import {
  Brain,
  Target,
  Trophy,
  Users,
  BookOpen,
  BarChart3,
  CheckCircle,
  Star,
  ArrowRight,
  Play,
  Zap,
  Shield,
  Clock,
  Award,
  TrendingUp,
  MessageSquare,
  Sparkles
} from 'lucide-react';

const fadeInUp = {
  initial: { opacity: 0, y: 60 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.6, ease: 'easeOut' as const }
};

const fadeInLeft = {
  initial: { opacity: 0, x: -60 },
  animate: { opacity: 1, x: 0 },
  transition: { duration: 0.6, ease: 'easeOut' as const }
};

const fadeInRight = {
  initial: { opacity: 0, x: 60 },
  animate: { opacity: 1, x: 0 },
  transition: { duration: 0.6, ease: 'easeOut' as const }
};

const staggerContainer = {
  animate: {
    transition: {
      staggerChildren: 0.1
    }
  }
};

const scaleIn = {
  initial: { opacity: 0, scale: 0.8 },
  animate: { opacity: 1, scale: 1 },
  transition: { duration: 0.5, ease: 'easeOut' as const }
};

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-white">
      {/* Header */}
      <motion.header 
        className="fixed top-0 w-full bg-white/80 backdrop-blur-md border-b border-gray-200 z-50"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                <Brain className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold text-gray-900">Gabarita.AI</span>
            </div>
            <nav className="hidden md:flex space-x-8">
              <a href="#recursos" className="text-gray-600 hover:text-gray-900 transition-colors">Recursos</a>
              <a href="#planos" className="text-gray-600 hover:text-gray-900 transition-colors">Planos</a>
              <a href="#depoimentos" className="text-gray-600 hover:text-gray-900 transition-colors">Depoimentos</a>
              <a href="#contato" className="text-gray-600 hover:text-gray-900 transition-colors">Contato</a>
            </nav>
            <div className="flex items-center space-x-4">
              <Button variant="ghost" onClick={() => window.location.href = '/login'}>Entrar</Button>
            <Button className="bg-blue-600 hover:bg-blue-700" onClick={() => window.location.href = '/signup'}>Começar Grátis</Button>
            </div>
          </div>
        </div>
      </motion.header>

      {/* Hero Section */}
      <section className="pt-24 pb-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center">
            <motion.div
              className="inline-flex items-center px-4 py-2 bg-blue-50 rounded-full text-blue-700 text-sm font-medium mb-8"
              {...fadeInUp}
            >
              <Sparkles className="w-4 h-4 mr-2" />
              Revolucione seus estudos para concursos
            </motion.div>
            
            <motion.h1 
              className="text-4xl md:text-6xl font-bold text-gray-900 mb-6 leading-tight"
              {...fadeInUp}
              transition={{ delay: 0.1, duration: 0.6 }}
            >
              Prepare-se para o{' '}
              <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                CNU
              </span>{' '}
              com{' '}
              <span className="bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                Inteligência Artificial
              </span>
            </motion.h1>
            
            <motion.p 
              className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto"
              {...fadeInUp}
              transition={{ delay: 0.2, duration: 0.6 }}
            >
              A plataforma mais avançada para estudar para concursos públicos. 
              Questões personalizadas, simulados inteligentes e correção automática de redações.
            </motion.p>
            
            <motion.div 
              className="flex flex-col sm:flex-row gap-4 justify-center items-center"
              {...fadeInUp}
              transition={{ delay: 0.3, duration: 0.6 }}
            >
              <Button size="lg" className="bg-blue-600 hover:bg-blue-700 text-lg px-8 py-4" onClick={() => window.location.href = '/signup'}>
                <Play className="w-5 h-5 mr-2" />
                Começar Agora - Grátis
              </Button>
              <Button variant="outline" size="lg" className="text-lg px-8 py-4" onClick={() => window.location.href = '/demo'}>
                Ver Demonstração
                <ArrowRight className="w-5 h-5 ml-2" />
              </Button>
            </motion.div>
            
            <motion.div 
              className="mt-12 text-sm text-gray-500"
              {...fadeInUp}
              transition={{ delay: 0.4, duration: 0.6 }}
            >
              ✨ 3 questões grátis • Sem cartão de crédito • Cancele quando quiser
            </motion.div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <motion.section 
        className="py-16 bg-gray-50"
        initial="initial"
        whileInView="animate"
        viewport={{ once: true }}
        variants={staggerContainer}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {[
              { number: "50K+", label: "Questões Disponíveis", icon: BookOpen },
              { number: "95%", label: "Taxa de Aprovação", icon: Trophy },
              { number: "10K+", label: "Estudantes Ativos", icon: Users },
              { number: "4.9/5", label: "Avaliação dos Usuários", icon: Star }
            ].map((stat, index) => (
              <motion.div 
                key={index}
                className="text-center"
                variants={scaleIn}
                transition={{ delay: index * 0.1 }}
              >
                <div className="inline-flex items-center justify-center w-12 h-12 bg-blue-100 rounded-lg mb-4">
                  <stat.icon className="w-6 h-6 text-blue-600" />
                </div>
                <div className="text-3xl font-bold text-gray-900 mb-2">{stat.number}</div>
                <div className="text-gray-600">{stat.label}</div>
              </motion.div>
            ))}
          </div>
        </div>
      </motion.section>

      {/* Features Section */}
      <section id="recursos" className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <motion.div 
            className="text-center mb-16"
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
            variants={fadeInUp}
          >
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Recursos que fazem a diferença
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Tecnologia de ponta para maximizar seu desempenho nos estudos
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                icon: Brain,
                title: "IA Personalizada",
                description: "Algoritmos inteligentes que se adaptam ao seu ritmo de aprendizado e identificam suas dificuldades.",
                color: "from-blue-500 to-cyan-500"
              },
              {
                icon: Target,
                title: "Questões Direcionadas",
                description: "Banco com mais de 50.000 questões organizadas por matéria, banca e nível de dificuldade.",
                color: "from-purple-500 to-pink-500"
              },
              {
                icon: BarChart3,
                title: "Análise de Desempenho",
                description: "Relatórios detalhados com estatísticas de acertos, tempo de resposta e evolução.",
                color: "from-green-500 to-emerald-500"
              },
              {
                icon: MessageSquare,
                title: "Correção de Redação",
                description: "IA especializada em correção de redações com feedback detalhado e sugestões de melhoria.",
                color: "from-orange-500 to-red-500"
              },
              {
                icon: Clock,
                title: "Simulados Cronometrados",
                description: "Simule as condições reais da prova com cronômetro e ambiente similar ao concurso.",
                color: "from-indigo-500 to-purple-500"
              },
              {
                icon: Shield,
                title: "Plano de Estudos",
                description: "Cronograma personalizado baseado no tempo disponível e no concurso escolhido.",
                color: "from-teal-500 to-cyan-500"
              }
            ].map((feature, index) => (
              <motion.div
                key={index}
                className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 hover:shadow-lg transition-all duration-300"
                initial="initial"
                whileInView="animate"
                viewport={{ once: true }}
                variants={index % 2 === 0 ? fadeInLeft : fadeInRight}
                transition={{ delay: index * 0.1 }}
                whileHover={{ y: -5 }}
              >
                <div className={`inline-flex items-center justify-center w-12 h-12 bg-gradient-to-r ${feature.color} rounded-lg mb-6`}>
                  <feature.icon className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-4">{feature.title}</h3>
                <p className="text-gray-600 leading-relaxed">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <motion.section 
        className="py-20 bg-gradient-to-r from-blue-600 to-purple-600"
        initial="initial"
        whileInView="animate"
        viewport={{ once: true }}
        variants={fadeInUp}
      >
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
            Pronto para revolucionar seus estudos?
          </h2>
          <p className="text-xl text-blue-100 mb-8">
            Junte-se a milhares de estudantes que já estão usando a IA para passar em concursos
          </p>
          <Button size="lg" className="bg-white text-blue-600 hover:bg-gray-100 text-lg px-8 py-4" onClick={() => window.location.href = '/signup'}>
            <Zap className="w-5 h-5 mr-2" />
            Começar Gratuitamente
          </Button>
        </div>
      </motion.section>

      {/* Pricing Section */}
      <section id="planos" className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <motion.div 
            className="text-center mb-16"
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
            variants={fadeInUp}
          >
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Planos para todos os perfis
            </h2>
            <p className="text-xl text-gray-600">
              Escolha o plano ideal para sua jornada de estudos
            </p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            {[
              {
                name: "Trial Free",
                price: "R$ 2,99",
                period: "3 questões",
                description: "Experimente nossa plataforma",
                features: [
                  "3 questões gratuitas",
                  "Acesso básico à plataforma",
                  "Correção automática",
                  "Estatísticas básicas"
                ],
                popular: false,
                buttonText: "Começar Grátis",
                buttonVariant: "outline" as const
              },
              {
                name: "Black CNU",
                price: "R$ 97",
                period: "/mês",
                description: "Para quem quer passar no CNU",
                features: [
                  "Questões ilimitadas",
                  "Simulados completos",
                  "Correção de redação IA",
                  "Plano de estudos personalizado (Em breve)",
                  "Análise detalhada de desempenho",
                  "Suporte prioritário"
                ],
                popular: true,
                buttonText: "Assinar Agora",
                buttonVariant: "default" as const
              },
              {
                name: "Premium",
                price: "R$ 197",
                period: "/mês",
                description: "Acesso completo a todos os concursos",
                features: [
                  "Todos os recursos do Black CNU",
                  "Acesso a todos os concursos",
                  "Mentoria individual",
                  "Grupos de estudo exclusivos",
                  "Material complementar",
                  "Garantia de aprovação*"
                ],
                popular: false,
                buttonText: "Assinar Premium",
                buttonVariant: "outline" as const
              }
            ].map((plan, index) => (
              <motion.div
                key={index}
                className={`relative bg-white p-8 rounded-2xl border-2 transition-all duration-300 hover:shadow-xl ${
                  plan.popular 
                    ? 'border-blue-500 shadow-lg scale-105' 
                    : 'border-gray-200 hover:border-blue-300'
                }`}
                initial="initial"
                whileInView="animate"
                viewport={{ once: true }}
                variants={scaleIn}
                transition={{ delay: index * 0.1 }}
                whileHover={{ y: -5 }}
              >
                {plan.popular && (
                  <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                    <span className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-4 py-2 rounded-full text-sm font-medium">
                      Mais Popular
                    </span>
                  </div>
                )}
                
                <div className="text-center mb-8">
                  <h3 className="text-2xl font-bold text-gray-900 mb-2">{plan.name}</h3>
                  <p className="text-gray-600 mb-4">{plan.description}</p>
                  <div className="flex items-baseline justify-center">
                    <span className="text-4xl font-bold text-gray-900">{plan.price}</span>
                    <span className="text-gray-600 ml-1">{plan.period}</span>
                  </div>
                </div>
                
                <ul className="space-y-4 mb-8">
                  {plan.features.map((feature, featureIndex) => (
                    <li key={featureIndex} className="flex items-center">
                      <CheckCircle className="w-5 h-5 text-green-500 mr-3 flex-shrink-0" />
                      <span className="text-gray-700">{feature}</span>
                    </li>
                  ))}
                </ul>
                
                <Button 
                  variant={plan.buttonVariant}
                  size="lg" 
                  className={`w-full ${
                    plan.popular 
                      ? 'bg-blue-600 hover:bg-blue-700 text-white' 
                      : ''
                  }`}
                  onClick={() => window.location.href = '/signup'}
                >
                  {plan.buttonText}
                </Button>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section id="depoimentos" className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div 
            className="text-center mb-16"
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
            variants={fadeInUp}
          >
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              O que nossos alunos dizem
            </h2>
            <p className="text-xl text-gray-600">
              Histórias reais de quem conquistou a aprovação
            </p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                name: "Maria Silva",
                role: "Estudante CNU 2025",
                content: "O Gabarita.AI tem uma abordagem inovadora! A IA identifica exatamente onde tenho dificuldades e me ajuda a focar nos pontos certos para melhorar.",
                rating: 5
              },
              {
                name: "João Santos",
                role: "Concurseiro",
                content: "Plataforma muito bem estruturada! Os simulados são bem elaborados e a correção de redação com IA é uma funcionalidade excelente.",
                rating: 5
              },
              {
                name: "Ana Costa",
                role: "Estudante de Concursos",
                content: "Estou impressionada com a qualidade da plataforma. A personalização do estudo realmente faz diferença no meu aprendizado.",
                rating: 5
              }
            ].map((testimonial, index) => (
              <motion.div
                key={index}
                className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100"
                initial="initial"
                whileInView="animate"
                viewport={{ once: true }}
                variants={fadeInUp}
                transition={{ delay: index * 0.1 }}
              >
                <div className="flex items-center mb-4">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <Star key={i} className="w-5 h-5 text-yellow-400 fill-current" />
                  ))}
                </div>
                <p className="text-gray-700 mb-6 leading-relaxed">"{testimonial.content}"</p>
                <div className="flex items-center">
                  <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center text-white font-semibold mr-4">
                    {testimonial.name.charAt(0)}
                  </div>
                  <div>
                    <div className="font-semibold text-gray-900">{testimonial.name}</div>
                    <div className="text-gray-600 text-sm">{testimonial.role}</div>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-2 mb-6">
                <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                  <Brain className="w-5 h-5 text-white" />
                </div>
                <span className="text-xl font-bold">Gabarita.AI</span>
              </div>
              <p className="text-gray-400 mb-6">
                A plataforma de estudos mais avançada do Brasil para concursos públicos.
              </p>
            </div>
            
            <div>
              <h3 className="font-semibold mb-4">Produto</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">Recursos</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Planos</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Simulados</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Redação IA</a></li>
              </ul>
            </div>
            
            <div>
              <h3 className="font-semibold mb-4">Suporte</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">Central de Ajuda</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Contato</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Status</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Comunidade</a></li>
              </ul>
            </div>
            
            <div>
              <h3 className="font-semibold mb-4">Legal</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">Privacidade</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Termos</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Cookies</a></li>
              </ul>
            </div>
          </div>
          
          <div className="border-t border-gray-800 mt-12 pt-8 text-center text-gray-400">
            <p>&copy; 2024 Gabarita.AI. Todos os direitos reservados.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}