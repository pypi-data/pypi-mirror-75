#include "AutoTestImpl.h"
#include "AutoTest.h"

#include <direct.h>

#include <glew.h>
#include <gl/gl.h>
#include <gl/glu.h>

#define STB_IMAGE_WRITE_IMPLEMENTATION
#define STB_IMAGE_WRITE_STATIC
#include <stb_image_write.h>

namespace autotest
{
	static void FlipRGBAY(uint8_t* data, int width, int height)
	{
		uint8_t rgb[4];

		for (int y = 0; y < height / 2; ++y)
		{
			for (int x = 0; x < width; ++x)
			{
				int top = (x + y * width) * 4;
				int bottom = (x + (height - y - 1) * width) * 4;

				memcpy(rgb, data + top, sizeof(rgb));
				memcpy(data + top, data + bottom, sizeof(rgb));
				memcpy(data + bottom, rgb, sizeof(rgb));
			}
		}
	}

	static void ReadPixels(uint8_t*& data, int& width, int& height) {
		GLint viewport[4];
		glGetIntegerv(GL_VIEWPORT, viewport);

		int x = viewport[0];
		int y = viewport[1];
		width = viewport[2];
		height = viewport[3];

		if (data == nullptr)
		{
			data = (uint8_t*)malloc(width * height * 4 * sizeof(uint8_t));
		}
		if (!data)
			return;

		glFlush();
		glReadBuffer(GL_BACK);
		glReadPixels(x, y, width, height, GL_RGBA, GL_UNSIGNED_BYTE, data);

		for (int i = 0; i < width * height; i++) {
			data[i * 4 + 3] = 255;
		}
	}
}

AutoTestImpl::AutoTestImpl()
{
	_mkdir("GameLoopResults");
}

AutoTestImpl::~AutoTestImpl()
{
}

void AutoTestImpl::FinishLoop()
{
    
}

void AutoTestImpl::Screenshots(const char* name)
{
    uint8_t* data = nullptr;
	int width, height;
	autotest::ReadPixels(data, width, height);
	if (data)
	{		
		char path[64];
		sprintf(path, "GameLoopResults/%s.png", name);
		autotest::FlipRGBAY(data, width, height);
		int result = stbi_write_png(path, width, height, 4, data, 0);
		free(data);
	}
}

const char* AutoTestImpl::GetResultPath()
{
    return "GameLoopResults/result.json";
}
