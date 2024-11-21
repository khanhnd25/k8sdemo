import pika

# Kết nối RabbitMQ
def get_rabbitmq_channel():
    # Cấu hình RabbitMQ
    connection_params = pika.ConnectionParameters(
        host="rabbitmq",  # Địa chỉ RabbitMQ (chỉnh lại nếu cần)
        heartbeat=30,  # Heartbeat để giữ kết nối ổn định
        blocked_connection_timeout=300
    )
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    # Khai báo queue (nếu chưa tồn tại)
    # channel.queue_declare(queue="my_queue", durable=True)
    
    return connection, channel