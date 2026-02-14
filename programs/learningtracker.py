import csv
from datetime import datetime, date

def visualize_progress(file_path):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("Matplotlib is not installed. To enable graphs, install it with: 'pip install matplotlib'")
        return

    timestamps = []
    percentages = []

    try:
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2:
                    try:
                        ts = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
                        pct = float(row[1])
                        timestamps.append(ts)
                        percentages.append(pct)
                    except (ValueError, TypeError):
                        # Skip malformed rows
                        continue
    except FileNotFoundError:
        print("No progress file found yet. Add some progress first.")
        return

    if not timestamps:
        print("No progress data to plot yet.")
        return

    regression_line_dates = None
    regression_line_values = None
    estimated_completion = None

    if len(timestamps) >= 2:
        numeric_dates = [ts.timestamp() for ts in timestamps]
        mean_x = sum(numeric_dates) / len(numeric_dates)
        mean_y = sum(percentages) / len(percentages)
        numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(numeric_dates, percentages))
        denominator = sum((x - mean_x) ** 2 for x in numeric_dates)
        if denominator != 0:
            slope = numerator / denominator
            intercept = mean_y - slope * mean_x

            latest_ts = max(numeric_dates)
            line_end_ts = latest_ts
            line_end_value = slope * latest_ts + intercept

            if slope > 0:
                completion_ts = (100 - intercept) / slope
                if completion_ts > latest_ts:
                    estimated_completion = datetime.fromtimestamp(completion_ts)
                    line_end_ts = completion_ts
                    line_end_value = 100

            line_start_ts = min(numeric_dates)
            line_start_value = slope * line_start_ts + intercept
            regression_line_dates = [datetime.fromtimestamp(line_start_ts), datetime.fromtimestamp(line_end_ts)]
            regression_line_values = [line_start_value, line_end_value]

    plt.figure(figsize=(9, 5))
    plt.plot(timestamps, percentages, marker='o', linewidth=2, color='#1f77b4')
    plt.title('Course Progress Over Time')
    plt.xlabel('Date')
    plt.ylabel('Completion (%)')
    plt.ylim(0, 100)
    plt.grid(True, linestyle='--', alpha=0.4)

    if regression_line_dates and regression_line_values:
        plt.plot(regression_line_dates, regression_line_values, linestyle='--', color='#ff7f0e', label='Trendline')
        if estimated_completion:
            plt.scatter(estimated_completion, 100, color='#2ca02c', zorder=5)
            plt.annotate(
                f"Est. finish: {estimated_completion.strftime('%b %d, %Y')}",
                xy=(estimated_completion, 100),
                xytext=(10, -25),
                textcoords='offset points',
                arrowprops=dict(arrowstyle='->', color='#2ca02c')
            )
        plt.legend()

    if estimated_completion:
        print(f"Estimated completion date based on current trend: {estimated_completion.strftime('%B %d, %Y')}")

    plt.tight_layout()
    try:
        plt.show()
    except Exception as e:
        print(f"Unable to display the graph: {e}")

# Constants
END_DATE = date(2025, 12, 31)

def read_last_progress(file_path):
    try:
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            if rows:
                return float(rows[-1][1])  # Return the last percentage
    except FileNotFoundError:
        pass
    return 0.0  # Default if no file exists

def write_progress(file_path, percentage):
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), percentage])

def calculate_daily_effort(current_percentage):
    today = date.today()
    days_left = (END_DATE - today).days
    return (100 - current_percentage) / days_left if days_left > 0 else 0

def main():
    file_path = "progress.csv"
    last_progress = read_last_progress(file_path)
    
    print("Have you studied recently? (yes/no)")
    answer = input().strip().lower()
    
    if answer == "yes":
        print("What is your current course completion percentage?")
        try:
            current_percentage = float(input().strip())
        except ValueError:
            print("Invalid number. Please enter a numeric percentage like 42.5")
            return
        progress_difference = current_percentage - last_progress
        
        write_progress(file_path, current_percentage)
        
        if progress_difference > 0:
            daily_effort = calculate_daily_effort(current_percentage)
            print(f"Great job! You've made {progress_difference:.2f}% progress.")
            print(f"To finish your course by {END_DATE.strftime('%B %d, %Y')}, you need to put in at least {daily_effort:.2f}% effort daily.")
        else:
            print("No progress detected. Keep it up!")
    else:
        today = date.today()
        days_left = (END_DATE - today).days
        print(f"There are {days_left} days left until {END_DATE.strftime('%B %d, %Y')}. Keep going!")

    # Optional: visualize progress at the end
    print("\nWould you like to visualize your progress in a graph now? (yes/no)")
    show_graph = input().strip().lower()
    if show_graph == 'yes':
        visualize_progress(file_path)

if __name__ == "__main__":
    main()
