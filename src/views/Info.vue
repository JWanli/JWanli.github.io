<template>
  <div class="page-container info-page">
    <main class="info-main">
      <div class="header">
        <h2 class="title">📚 界面功能</h2>
        <p class="subtitle">大枪等级分系统说明</p>
      </div>

      <div class="cards-layout">
        <section id="rank-card" class="info-anchor">
          <el-card class="info-card" shadow="hover">
            <template #header>
              <div class="card-header">
                <h3>📊 排名页</h3>
              </div>
            </template>
            <div class="card-body">
              <ul class="bullet-list">
                <li class="text-body"><strong>【地区】</strong>通常为城市，也可能为省、县，总之以选手自我认同的地区名称作显示。</li>
                <li class="text-body"><strong>【位序】</strong>对应右上角的优先排序，默认活跃优先（显示为 Elo↓活跃▼），点击后切换至 Elo 优先（显示为 Elo▼活跃↓）。</li>
                <li class="text-body"><strong>【选手名】</strong>为选手实名+昵称（灰色），无实名选手直接显示昵称。</li>
                <li class="text-body"><strong>【Elo】</strong>Elo等级分为国际通用的竞技预测评分系统，大枪等级分采用的具体算法包含若干修正，详见后文“公式汇总”部分。</li>
                <li class="text-body"><strong>【活跃】</strong>刻画选手在长时段内参赛情况的数值，也可看作对Elo分的可靠性测量，详见后文“公式汇总”部分。</li>
                <li class="text-body">&nbsp;点击任意选手行，可展开选手详细信息，包括所在团队、更新时间、Elo峰值、峰值时间以及赛事成绩等。</li>
                <li class="text-body">&nbsp;选手名前方的 &nbsp; <span class="inline-change" aria-hidden="true"><span class="rank-change-up">↑</span> <span class="rank-change-down">↓</span> <span class="rank-change-new">+</span></span> 图标代表其位序在最新更新中发生了变动（上升、下降、新入榜），<span class="rank-change-up">↑</span> <span class="rank-change-down">↓</span> 仅在右上角排序为 分数 优先（显示为：分数▼）时才会显示。注意：被动改变位序（因他人位序变化）不会显示图标。</li>
                <li class="text-body">&nbsp;选手荣誉称号（显示在选手名称后方的彩色图标）含义取决于认证称号的组织团体，如：枪法武艺联盟（枪武联）的武艺共识评价（已录入），国际大枪机构（IDO）的枪士制度（待录入）。</li>
              </ul>
            </div>
          </el-card>
        </section>

        <section id="formula-card" class="info-anchor">
          <el-card class="info-card" shadow="hover">
            <template #header>
              <div class="card-header">
                <h3>📐 公式汇总</h3>
              </div>
            </template>
            <div class="card-body">
              <div class="rule-section">
                <h4 class="sub-title ">ELO 等级分</h4>
                <p class="text-body">Elo等级分是一种用于计算相对竞技水平的评分系统，广泛应用于棋类、电子竞技、体育比赛等场景。</p>
                <p class="text-body">其核心思想是：赛前根据双方分差计算预期胜率；根据结果与胜率差值调整分数；好于预期则加分，反之减分；差距越大，分数改变量越大。</p>
                <p class="text-body">选手A的预期胜率公式：</p>
                <div class="math-formula" v-pre>
                  \[ E_A = \frac{1}{1 + 10^{(R_B - R_A) / 400}} \]
                </div>
                <p class="text-body">选手A的等级分更新公式：</p>
                <div class="math-formula" v-pre>
                  \[ R_A' = R_A + K \times (S_A - E_A) \]
                </div>
                <p class="text-body text-note">K的取值：通常为32，在大枪等级分的计算中我们根据比赛中每局的回合数（或折算回合数）来确定K值。</p>
                <p class="text-body">以下为已使用的不同比赛类型：</p>
                <ul class="event-list text-body">
                  <li>1回合：K=8</li>
                  <li>3回合：K=16</li>
                  <li>2本制：K=20</li>
                  <li>5回合：K=24</li>
                  <li>7回合：K=32</li>
                  <li>满5回合：K=32</li>
                  <li>最小回合数≥4：K=32</li>
                </ul>
                <p class="text-body">当一场比赛包含多局时（如：三局两胜制），每局比赛独立计算分数。</p>
                <p class="text-body">注：两位选手间的一次比赛为“场”，由休息时间分割的比赛流程为“局”，每一次计分结算为“回合”。即：场＞局＞回合。</p>
                <p class="text-body">S的取值：通常采用 胜1 负0 平0.5 计分，在大枪等级分的计算中使用了略特殊的方式。</p>

                <div class="spacer" aria-hidden="true"></div>
                <h4 class="sub-title">大枪等级分专属机制</h4>
                <p class="text-body">比赛结果S根据比分与赛制进行计算：</p>
                <p class="text-body">记比赛结果（单局）分数为P。</p>
                <p class="text-body">固定回合数赛制：无论提前结束或加赛回合，记实际比赛回合数为C，存在得分的回合数为G。</p>
                <p class="text-body">选手A的比赛结果公式：</p>
                <div class="math-formula" v-pre>
                  \[ S_A = \frac{P_A}{P_A + P_B} \times \frac{G}{C} + \frac{C - G}{C \times 2} \]
                </div>
                <p class="text-body">固定上限分赛制：无论加分制或减分制，记上限分为Q。</p>
                <p class="text-body">选手A的比赛结果公式：</p>
                <div class="math-formula" v-pre>
                  \[ S_A = \frac{P_A + Q - P_B}{Q \times 2} \]
                </div>
                <p class="text-body text-note">允许P＞Q或P＜0</p>
                <p class="text-body">还有其它一些机制用以适配当下大枪技击运动发展情况：</p>
                <ul class="event-list text-body">
                  <li>比赛中与非同城同团体对手交手将额外获得等级分：对手赛后等级分的1/600。</li>
                  <li>选手活跃值过低且赛后等级分变更值较大时，可能触发重新定级，即作为无等级分选手计算。</li>
                  <li>若比赛中有无等级分选手参赛，首先在等级分选手间计算赛后值，根据该值定级新选手作为其赛前值，最后重新以赛前值计算全部选手赛后值。</li>
                </ul>

                <div class="spacer" aria-hidden="true"></div>
                <h4 class="sub-title">活跃值</h4>
                <p class="text-body">活跃值计算与三要素相关：</p>
                <ul class="event-list text-body">
                  <li>最近更新时间至当前时间的天数：时间越久活跃值越低。</li>
                  <li>在交手网络中的位置：统计每个选手与其它选手是否有过交手记录，与最多高等级分选手交手过的选手置为第0层（≠最高分选手），与他（们）交手过的为第1层，依次类推。每增加一个新的交手对手可以增加自身权重，但增量系数由对手所在层决定，层越小系数越大，同层对手的累加值有上限，层越小上限越高。</li>
                  <li>当前等级分：当选手等级分越高时，活跃值的自然衰减速度会越慢（因为预期低分选手的等级分在长期不参赛下的不确定性更大），即越不容易触发重新定级。</li>
                </ul>
              </div>
            </div>
          </el-card>
        </section>

        <section id="event-card" class="info-anchor">
          <el-card class="info-card" shadow="hover">
            <template #header>
              <div class="card-header">
                <h3>🏆 赛事信息</h3>
              </div>
            </template>
            <div class="card-body">
              <p class="text-body">按拼音顺序排列（括号中为录入起始年份）：</p>
              <ul class="event-list text-body">
                <li>北斗历史剑术联盟大枪示范赛（2021）</li>
                <li>北京市大枪公开赛（2025）</li>
                <li>长三角中国武道文化节大枪赛（2025）</li>
                <li>成都览山鉴水兵击赛长枪赛（2024）</li>
                <li>钢铁友谊杯国际剑术公开赛大枪赛（2026）</li>
                <li>华步杯首届大枪赛（2026）</li>
                <li>君迁杯传统大枪对抗赛（2022）</li>
                <li>南京国际大枪竞赛（2024）</li>
                <li>宁波IDO国际大枪邀请赛（2025）</li>
                <li>戚继光杯国际大枪竞赛（2025）</li>
                <li>上海大枪交流会（2024）</li>
                <li>上海大枪赛（2019）</li>
                <li>台湾IDO大枪赛（2023）</li>
                <li>台湾八极拳协会大枪技击赛（2023）</li>
                <li>台湾世界杯武术锦标赛大枪赛（2023）</li>
                <li>台湾中正杯大枪技击赛（2025）</li>
                <li>香港大枪竞技邀请赛（2024）</li>
                <li>一搏成名国术会长兵大枪争霸赛（2025）</li>
                <li>驭龙杯古典武艺大枪公开赛（2023）</li>
              </ul>
              <p class="text-body">上述比赛成绩已采纳为大枪等级分计算数据来源，实际使用数据来自赛事主办方或参赛选手提供（部分赛事成绩不完整）。</p>
              <p class="text-body contact-text">如果您希望录入新的比赛，或提供比赛成绩（完整或局部），可添加微信：<strong>mymcyyt</strong>（申请注明“大枪”）。</p>
            </div>
          </el-card>
        </section>
      </div>
    </main>

    <aside class="toc-panel" aria-label="页面目录">
      <div class="toc-title">目录</div>
      <button class="toc-item" type="button" @click="scrollToSection('rank-card')">
        <span class="toc-label toc-label-desktop">📊 排名页</span>
        <span class="toc-label toc-label-mobile">📊 排名</span>
      </button>
      <button class="toc-item" type="button" @click="scrollToSection('formula-card')">
        <span class="toc-label toc-label-desktop">📐 公式汇总</span>
        <span class="toc-label toc-label-mobile">📐 公式</span>
      </button>
      <button class="toc-item" type="button" @click="scrollToSection('event-card')">
        <span class="toc-label toc-label-desktop">🏆 赛事信息</span>
        <span class="toc-label toc-label-mobile">🏆 赛事</span>
      </button>
    </aside>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'

const scrollToSection = (id) => {
  const element = document.getElementById(id)
  if (!element) return

  const offset = window.innerWidth <= 768 ? 90 : 88
  const top = window.scrollY + element.getBoundingClientRect().top - offset
  window.scrollTo({ top, behavior: 'smooth' })
}

const initMathJax = () => {
  window.MathJax = {
    tex: {
      inlineMath: [['\\(', '\\)']],
      displayMath: [['\\[', '\\]']]
    },
    startup: { typeset: false }
  }

  const script = document.createElement('script')
  script.src = 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js'
  script.async = true
  document.head.appendChild(script)

  script.onload = () => {
    if (window.MathJax && window.MathJax.typesetPromise) {
      window.MathJax.typesetPromise()
    }
  }
}

onMounted(() => {
  initMathJax()
})
</script>

<style scoped>
.info-page {
  max-width: 1240px;
  margin: 0 auto;
  padding: 36px 24px 36px 24px;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: var(--el-text-color-regular);
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: 24px;
  align-items: start;
}

.info-main {
  min-width: 0;
  max-width: 960px;
  width: 100%;
  margin: 0 auto;
}

.header {
  text-align: center;
  margin-bottom: 36px;
}

.title {
  font-size: 30px;
  color: var(--el-text-color-primary);
  margin-bottom: 6px;
  font-weight: 800;
  letter-spacing: -0.3px;
}

.subtitle {
  color: var(--el-text-color-secondary);
  font-size: 15px;
  font-weight: 500;
  margin-bottom: 6px;
}

.cards-layout {
  display: flex;
  flex-direction: column;
  gap: 28px;
}

.info-anchor {
  scroll-margin-top: 24px;
}

.info-card {
  border-radius: 12px;
  border: 1px solid var(--el-border-color-lighter);
  background: var(--el-bg-color-overlay);
  overflow: hidden;
  box-shadow: 0 1px 0 rgba(15, 23, 42, 0.02);
}

.card-header {
  padding: 8px 20px;
  border-bottom: none;
  display: flex;
  align-items: center;
  justify-content: flex-start;
}

.card-header h3 {
  margin: 0;
  font-size: 22px;
  font-weight: 800;
  color: var(--el-text-color-primary);
  display: inline-block;
  padding: 0 6px;
  border-radius: 0;
  background: transparent;
  max-width: 78%;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.05;
}

.card-body {
  padding: 10px 20px;
  display: block;
}

.text-body {
  font-size: 15px;
  line-height: 1.9;
  color: var(--el-text-color-regular);
  margin: 0 0 12px 0;
  text-align: left;
  word-break: break-word;
  letter-spacing: 0.1px;
}

.text-note {
  font-size: 13px;
  color: var(--el-text-color-placeholder);
  margin-top: 8px;
}

.sub-title {
  font-size: 17px;
  font-weight: 700;
  color: var(--el-text-color-primary);
  margin: 12px 0 8px 0;
  padding-left: 12px;
  border-left: 4px solid var(--el-color-primary);
}

.rule-section {
  margin-top: 8px;
}

.math-formula {
  background-color: var(--el-fill-color-light);
  border: 1px solid var(--el-border-color-lighter);
  padding: 14px 18px;
  margin: 10px 0;
  border-radius: 10px;
  overflow-x: auto;
  font-size: 16px;
  text-align: center;
  color: var(--el-text-color-primary);
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.02);
}

.event-list {
  padding-left: 24px;
  margin-bottom: 12px;
}

.event-list li {
  margin-bottom: 10px;
}

.contact-text {
  background: var(--el-color-primary-light-9);
  padding: 12px 14px;
  border-radius: 8px;
  color: var(--el-color-primary);
  font-size: 15px;
}

.toc-panel {
  position: fixed;
  top: 120px;
  right: 24px;
  width: 180px;
  border: 1px solid var(--el-border-color-lighter);
  border-radius: 12px;
  background: var(--el-bg-color-overlay);
  padding: 14px 12px;
  box-shadow: 0 1px 0 rgba(15, 23, 42, 0.02);
  z-index: 10;
}

.toc-title {
  font-size: 13px;
  font-weight: 800;
  color: var(--el-text-color-primary);
  margin-bottom: 10px;
  padding-left: 4px;
}

.toc-item {
  width: 100%;
  border: none;
  background: transparent;
  color: var(--el-text-color-regular);
  text-align: left;
  padding: 10px 8px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 13px;
  line-height: 1.4;
}

.toc-label-mobile {
  display: none;
}

.toc-item:hover {
  background: var(--el-fill-color-light);
  color: var(--el-color-primary);
}

@media (max-width: 768px) {
  .info-page {
    padding: 8px 12px 20px 12px;
    grid-template-columns: 1fr;
  }

  .info-main {
    max-width: none;
    padding-top: 18px;
  }

  .title {
    font-size: 24px;
    margin-bottom: 2px;
  }

  .subtitle {
    margin-bottom: 0;
  }

  .math-formula {
    font-size: 15px;
    padding: 12px;
    text-align: left;
  }

  .card-header {
    padding: 12px;
  }

  .card-body {
    padding: 12px;
  }

  .card-header h3 {
    max-width: 100%;
  }

  .toc-panel {
    position: fixed;
    top: 70px;
    right: 8px;
    left: auto;
    width: 72px;
    display: flex;
    gap: 4px;
    flex-direction: column;
    align-items: center;
    margin-bottom: 0;
    padding: 8px 6px;
  }

  .toc-title {
    width: 100%;
    margin-bottom: 0;
    text-align: center;
    padding-left: 0;
  }

  .toc-item {
    width: 100%;
    flex: none;
    min-width: 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    padding: 6px 3px;
    text-align: center;
    font-size: 11px;
    line-height: 1.1;
  }

  .toc-label-desktop {
    display: none;
  }

  .toc-label-mobile {
    display: inline;
  }
}

html.dark .math-formula {
  background-color: var(--el-fill-color-darker);
  border-color: var(--el-border-color-dark);
}

html.dark .contact-text {
  background: rgba(64, 158, 255, 0.06);
}

.bullet-list {
  list-style: disc;
  padding-left: 20px;
  margin: 0;
}

.bullet-list .text-body {
  margin: 6px 0;
}

.spacer {
  height: 18px;
}

/* 与排行榜一致的颜色标记（inline 使用） */
.inline-change {
  display: inline-flex;
  gap: 6px;
  align-items: center;
  margin-right: 6px;
}
.inline-change .rank-change-up,
.rank-change-up {
  color: #67C23A; /* 绿色 */
  font-weight: 800;
}
.inline-change .rank-change-down,
.rank-change-down {
  color: #F56C6C; /* 红色 */
  font-weight: 800;
}
.inline-change .rank-change-new,
.rank-change-new {
  color: #E6A23C; /* 黄色 */
  font-weight: 800;
}
</style>